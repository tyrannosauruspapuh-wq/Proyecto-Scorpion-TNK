# Versión 4.2.0
# Código del ESP32 como "maestro" de la TANG NANO 9K.
# Haciendo uso de Micropython, se utiliza el módulo Wi-Fi para la comunicación con una PC de donde recibe los comandos traducidos del control de Xbox
# Se contempla el control de 2 motores de tracción, 2 servomotores de torreta y 2 motores de disparo con un módulo de Puente H L298N
# Recibe los datos por Wi-Fi, manda 8 bits a la FPGA en formato ASCII para los servos.
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA
# Autor: Hafid Cruz Molina, fecha: 02/06/2026.

import machine 
import socket 
import network 
import time 

# 1. Configuración de la UART para hablar con la FPGA
uart_fpga = machine.UART(1, baudrate=9600, tx=16, rx=17)

# --- Configuración de pines para el módulo L298N ---
# Asignamos 4 pines digitales del ESP32 configurados como salidas (OUT) para controlar la dirección de los 2 motores DC conectados al puente H.
in1 = machine.Pin(32, machine.Pin.OUT)
in2 = machine.Pin(33, machine.Pin.OUT)
in3 = machine.Pin(25, machine.Pin.OUT) 
in4 = machine.Pin(26, machine.Pin.OUT)

# Estado inicial: L298N apagado por seguridad
# Ponemos todos los pines en estado bajo (0V) para asegurar que los motores no giren al encender
in1.value(0); in2.value(0)
in3.value(0); in4.value(0)
# ----------------------------------------------------------

# 2. Configuración de Wi-Fi en Modo Access Point 
ap = network.WLAN(network.AP_IF)
ap.active(True) 
ap.config(essid="Tanque_WiFi", password="controltanque")

print("===========================================")
print("¡Red Wi-Fi del Tanque Iniciada!")
print("Conéctate a: Tanque_WiFi")
print("Contraseña:  controltanque")
print("IP del ESP32:", ap.ifconfig()[0])
print("===========================================")

# 3. Crear el Socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5005))

# Variable global para recordar qué servo (J o K) está esperando recibir su ángulo
servo_pendiente = None 

# Función auxiliar para empaquetar y enviar el comando de un servo a la FPGA
def enviar_angulo_fpga(cabecera, angulo, nombre_servo):
    # Valida que el ángulo no exceda el tamaño de un byte (0 a 255)
    if 0 <= angulo <= 255:
        uart_fpga.write(bytes([cabecera]))
        time.sleep_ms(2)
        # Envía el byte con el valor real del ángulo
        uart_fpga.write(bytes([angulo]))
        print(f"¡ENVIADO EXITOSO! -> FPGA <- Cabecera: {hex(cabecera)}, Valor: {angulo} (Servo {nombre_servo})")
    else:
        # Descarta el valor si está fuera de los límites aceptables
        print(f"Valor {angulo} fuera de rango (Debe ser 0-255)")

def procesar_comando(command):
    global servo_pendiente 
    
    # --- LÓGICA DEL MÓDULO L298N (GATILLO DERECHO) ---
    if command == 'T':
        # Motores girando en el mismo sentido (Adelante)
        # Se pone un pin en HIGH (1) y su par en LOW (0) para crear la diferencia de potencial
        in1.value(1); in2.value(0) # Motor A avanza
        in3.value(1); in4.value(0) # Motor B avanza
        print("L298N -> ACTIVADO (Motores DC Girando)")
        return
    elif command == 'H':
        # Frenar motores DC (Halt)
        # Al igualar el voltaje a 0 en todos los pines, los motores pierden energía y se detienen
        in1.value(0); in2.value(0)
        in3.value(0); in4.value(0)
        print("L298N -> DESACTIVADO")
        return

    # --- LÓGICA DE MOTORES (FPGA) ---
    if command == 'F':
        uart_fpga.write(bytes([0x01])) 
        print("FPGA <- 0x01 (Adelante)")
        return
    elif command == 'B':
        uart_fpga.write(bytes([0x02])) 
        print("FPGA <- 0x02 (Atrás)")
        return
    elif command == 'L':
        uart_fpga.write(bytes([0x03])) 
        print("FPGA <- 0x03 (Izquierda)")
        return
    elif command == 'R':
        uart_fpga.write(bytes([0x04])) 
        print("FPGA <- 0x04 (Derecha)")
        return
    elif command == 'S':
        uart_fpga.write(bytes([0x00]))
        print("FPGA <- 0x00 (Stop)")
        return

    # --- LÓGICA DE SERVOS ---
    if command == 'J':
        servo_pendiente = 'J' 
        return
    elif command == 'K':
        servo_pendiente = 'K'
        return

    # Si el comando es un bloque de puros números (ej. "180")
    if command.isdigit():
        angulo = int(command) 
        if servo_pendiente == 'J':
            enviar_angulo_fpga(0xAA, angulo, 'J') 
            servo_pendiente = None 
        elif servo_pendiente == 'K':
            enviar_angulo_fpga(0xBB, angulo, 'K')
            servo_pendiente = None 
        return

    command_clean = command.replace(" ", "") 
    if command_clean.startswith('J') or command_clean.startswith('K'):
        id_servo = command_clean[0] 
        try:
            angulo = int(command_clean[1:])
            cabecera = 0xAA if id_servo == 'J' else 0xBB
            enviar_angulo_fpga(cabecera, angulo, id_servo)
        except ValueError:
            pass

print("Esperando comandos por Wi-Fi/UDP...")

# Bucle principal infinito que mantiene al ESP32 a la escucha
while True:
    try:
        # recvfrom bloquea (o intenta leer) hasta recibir un máximo de 1024 bytes
        data, addr = s.recvfrom(1024)
        if data:
            # Decodifica los bytes a texto UTF-8, quita saltos de línea/espacios y fuerza mayúsculas
            command_recibido = data.decode().strip().upper()
            procesar_comando(command_recibido)
    except Exception:
        pass
