# Versión 1.0.0
# Script de Python que corre en una PC conectada por Wi-Fi al ESP32, donde se traducen los comandos del control de Xbox a los comandos ya establecidos en el microcontrolador
# Se contempla el control de 2 motores
# Manda los datos por Wi-Fi en 8 bits a la ESP32, que a su vez los reenvía a la FPGA
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA y la main.py 4.0.0 de la ESP32.
# Autor: Hafid Cruz Molina, fecha: 29/05/2026.

import socket  
import time    
import sys 
import threading 
import ctypes 

# Definición de la estructura de datos del control de Xbox (Mapeo de C a Python)
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", ctypes.c_ushort),      # Botones presionados (A, B, X, Y, flechas, etc.)
        ("bLeftTrigger", ctypes.c_ubyte),   # Gatillo izquierdo (LT)
        ("bRightTrigger", ctypes.c_ubyte),  # Gatillo derecho (RT)
        ("sThumbLX", ctypes.c_short),       # Eje X del joystick izquierdo (Izquierda/Derecha)
        ("sThumbLY", ctypes.c_short),       # Eje Y del joystick izquierdo (Arriba/Abajo)
        ("sThumbRX", ctypes.c_short),       # Eje X del joystick derecho
        ("sThumbRY", ctypes.c_short),       # Eje Y del joystick derecho
    ]

# Definición del estado general de XInput (incluye el número de paquete y los datos del control)
class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", ctypes.c_ulong), # Número de paquete para saber si el estado ha cambiado
        ("Gamepad", XINPUT_GAMEPAD), 
    ]

# Intento de cargar la librería dinámica (DLL) de XInput en Windows
try:
    xinput = ctypes.windll.xinput1_4 # Intenta cargar la versión más reciente (Windows 8+)
except:
    xinput = ctypes.windll.xinput1_3 # Si falla, intenta cargar la versión de compatibilidad (Windows 7)

# Función para leer el estado actual del control de Xbox
def obtener_joysticks():
    state = XINPUT_STATE()
    # Llama a la API de Windows para obtener el estado del control 0 (el primer jugador)
    resultado = xinput.XInputGetState(0, ctypes.byref(state))
    if resultado == 0: # 0 significa "ERROR_SUCCESS" (el control está conectado y se leyó bien)
        return state.Gamepad
    return None # Si devuelve otro número, el control no está conectado

# Configuración de red para comunicarse con el ESP32
ESP32_IP = "192.168.4.1"  # Dirección IP del microcontrolador ESP32
PORT = 5005               # Puerto UDP donde el ESP32 está escuchando los comandos

# Creación del socket de red (IPv4, UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variable global que almacena el comando actual del motor
estado_motor = b'S'

# Función que se ejecutará en un hilo (thread) en segundo plano
def ráfaga_motores():
    while True:
        try:
            sock.sendto(estado_motor, (ESP32_IP, PORT))
            time.sleep(0.05) 
        except Exception:
            break # Si hay un error de red crítico, sale del bucle del hilo

# Creación e inicio del hilo en segundo plano para enviar la "ráfaga" de comandos
# daemon=True significa que este hilo se cerrará automáticamente cuando el programa principal termine
hilo_red = threading.Thread(target=ráfaga_motores, daemon=True)
hilo_red.start()

print("=== PUENTE XBOX ➔ WI-FI (TANK, TORRETAS Y L298N) ===")

try:
    while True:
        # Lee el estado del control en cada iteración
        gamepad = obtener_joysticks()
        
        if gamepad is None:
            # Si el control se desconecta, se asegura de que el tanque se detenga
            estado_motor = b'S' 
            
        else:
            # ---------------------------------------------
            # 1. CONTROL DE MOTORES (JOYSTICK IZQUIERDO)
            # ---------------------------------------------
            # Lee los valores del eje Y y X del joystick izquierdo
            ly = gamepad.sThumbLY
            lx = gamepad.sThumbLX
            
            # Se aplica una "zona muerta" de 15000 y -15000 para evitar movimientos fantasma
            # El valor máximo de los joysticks ronda los 32767 a -32768
            if ly > 15000:
                nuevo_motor = b'F'  # Forward (Adelante)
            elif ly < -15000:
                nuevo_motor = b'B'  # Backward (Atrás)
            elif lx < -15000:
                nuevo_motor = b'L'  # Left (Izquierda)
            elif lx > 15000:
                nuevo_motor = b'R'  # Right (Derecha)
            else:
                nuevo_motor = b'S'  # Stop (Detenido) si el joystick está en el centro
                
            # Solo si el estado deseado es distinto al estado actual, lo actualiza e imprime
            if estado_motor != nuevo_motor:
                estado_motor = nuevo_motor
                print(f"Tanque -> {nuevo_motor.decode()}") 

        time.sleep(0.02) 

# Captura el evento de "Ctrl + C" en la consola para cerrar el programa limpiamente
except KeyboardInterrupt:
    print("\nSistema apagado.")
