# Versión 4.1.0
# Código del ESP32 como "maestro" de la TANG NANO 9K.
# Haciendo uso de Micropython, se utiliza el módulo Wi-Fi para la comunicación con una PC de donde recibe los comandos traducidos del control de Xbox
# Se contempla el control de 2 motores y 2 servomotores
# Recibe los datos por Wi-Fi, manda 8 bits a la FPGA en formato ASCII para los servos.
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA
# Autor: Hafid Cruz Molina, fecha: 01/06/2026.

import machine 
import socket  
import network
import time   

uart_fpga = machine.UART(1, baudrate=9600, tx=16, rx=17)

# 2. Configuración de Wi-Fi en Modo Access Point 

ap = network.WLAN(network.AP_IF)
ap.active(True) 

ap.config(essid="Tanque_WiFi", password="controltanque")

# Muestra en la consola los datos de la red para facilitar la conexión
print("===========================================")
print("¡Red Wi-Fi del Tanque Iniciada!")
print("Conéctate a: Tanque_WiFi")
print("Contraseña:  controltanque")
print("IP del ESP32:", ap.ifconfig()[0])
print("===========================================")

# 3. Crear el Socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Se enlaza el socket para escuchar en cualquier interfaz ('0.0.0.0') por el puerto 5005
s.bind(('0.0.0.0', 5005))

# Variable global para recordar qué servo se va a mover 
# (útil si el comando del motor y el ángulo llegan en paquetes separados)
servo_pendiente = None 

# Función auxiliar para enviar comandos complejos (2 bytes) a los servos vía FPGA
def enviar_angulo_fpga(cabecera, angulo, nombre_servo):
    # Verifica que el ángulo esté en el rango válido de un byte (0 a 255)
    if 0 <= angulo <= 255:
        # Envía primero el byte de "cabecera" (0xAA para J, 0xBB para K) para avisar a la FPGA qué servo es
        uart_fpga.write(bytes([cabecera]))
        time.sleep_ms(2) # Pequeña pausa de 2ms para darle tiempo a la FPGA de procesar el primer byte     
        # Envía el segundo byte que contiene el valor del ángulo
        uart_fpga.write(bytes([angulo]))
        print(f"¡ENVIADO EXITOSO! -> FPGA <- Cabecera: {hex(cabecera)}, Valor: {angulo} (Servo {nombre_servo})")
    else:
        # Si el valor excede 255, no lo envía para evitar errores en la trama de datos
        print(f"Valor {angulo} fuera de rango (Debe ser 0-255)")

# Función principal que traduce el texto recibido por Wi-Fi en instrucciones para la FPGA
def procesar_comando(command):
    global servo_pendiente 

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
    # Caso 1: Los datos llegan separados (Ej. llega 'J' y en el siguiente paquete llega '180')
    if command == 'J':
        servo_pendiente = 'J' # Recuerda que el siguiente número que llegue es para el servo J
        return
    elif command == 'K':
        servo_pendiente = 'K' # Recuerda que el siguiente número que llegue es para el servo K
        return

    # Si el comando recibido es puramente numérico (ej. "180")
    if command.isdigit():
        angulo = int(command) # Convierte el texto a un número entero
        # Si estábamos esperando el ángulo para el servo J
        if servo_pendiente == 'J':
            enviar_angulo_fpga(0xAA, angulo, 'J') # 0xAA es la cabecera/identificador del servo J
            servo_pendiente = None
        # Si estábamos esperando el ángulo para el servo K
        elif servo_pendiente == 'K':
            enviar_angulo_fpga(0xBB, angulo, 'K') # 0xBB es la cabecera/identificador del servo K
            servo_pendiente = None 
        return

    # Caso 2: Los datos llegan juntos en el mismo paquete (Ej. "J180" o "K 90")
    command_clean = command.replace(" ", "") # Elimina posibles espacios en blanco por seguridad
    if command_clean.startswith('J') or command_clean.startswith('K'):
        id_servo = command_clean[0] # Extrae la primera letra ('J' o 'K')
        try:
            # Extrae todo lo que está después de la primera letra y lo convierte a entero
            angulo = int(command_clean[1:])
            # Asigna la cabecera correcta dependiendo de la letra extraída
            cabecera = 0xAA if id_servo == 'J' else 0xBB
            # Envía los dos bytes (cabecera y ángulo) a la FPGA
            enviar_angulo_fpga(cabecera, angulo, id_servo)
        except ValueError:
            pass

print("Esperando comandos por Wi-Fi/UDP...")

while True:
    try:
        data, addr = s.recvfrom(1024)
        if data:
            command_recibido = data.decode().strip().upper()
            procesar_comando(command_recibido)
    except Exception:
        pass
