# Versión 4.0.0
# Código del ESP32 como "maestro" de la TANG NANO 9K.
# Haciendo uso de Micropython, se utiliza el módulo Wi-Fi para la comunicación con una PC de donde recibe los comandos traducidos del control de Xbox
# Se contempla el control de 2 motores
# Recibe los datos por Wi-Fi, manda 8 bits a la FPGA en formato ASCII para los servos.
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA
# Autor: Hafid Cruz Molina, fecha: 29/05/2026.

import machine 
import socket 
import network 
import time   

# 1. Configuración de la UART para hablar con la FPGA
uart_fpga = machine.UART(1, baudrate=9600, tx=16, rx=17)

# 2. Configuración de Wi-Fi en Modo Access Point 
# Se crea una interfaz de red en modo Punto de Acceso (AP), para que el ESP32 emita su propia red Wi-Fi.
ap = network.WLAN(network.AP_IF)
ap.active(True) # Se enciende el punto de acceso
# Se configura el nombre de la red (SSID) y la contraseña para conectarse a ella
ap.config(essid="Tanque_WiFi", password="controltanque")

# Bloque de impresión para mostrar los datos de conexión en la consola serial (útil para depuración)
print("===========================================")
print("¡Red Wi-Fi del Tanque Iniciada!")
print("Conéctate a: Tanque_WiFi")
print("Contraseña:  controltanque")
# ap.ifconfig()[0] obtiene y muestra la dirección IP que se le asignó al ESP32 (usualmente 192.168.4.1)
print("IP del ESP32:", ap.ifconfig()[0])
print("===========================================")

# 3. Crear el Socket UDP
# Se crea un socket IPv4 (AF_INET) y de tipo UDP (SOCK_DGRAM), ideal para latencia baja
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind enlaza el socket a la dirección '0.0.0.0' (escucha en todas las interfaces) y al puerto 5005
s.bind(('0.0.0.0', 5005))

# Función que traduce las letras recibidas por Wi-Fi en bytes para enviarlos a la FPGA
def procesar_comando(command):

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

print("Esperando comandos por Wi-Fi/UDP...")

# Bucle principal infinito para escuchar los paquetes de red entrantes
while True:
    try:
        # Intenta recibir hasta 1024 bytes de datos del socket. 
        # recvfrom devuelve los datos (data) y la dirección del remitente (addr)
        data, addr = s.recvfrom(1024)
        if data:
            # Si llegan datos, los decodifica de bytes a texto, quita espacios en blanco (strip) y los convierte a mayúsculas
            command_recibido = data.decode().strip().upper()
            # Pasa la letra procesada a la función para que la envíe a la FPGA
            procesar_comando(command_recibido)
    except Exception:
        # Si ocurre algún error en la recepción (como un problema de red), lo ignora y sigue el bucle
        pass
