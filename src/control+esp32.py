# Versión 1.2.0
# Script de Python que corre en una PC conectada por Wi-Fi al ESP32, donde se traducen los comandos del control de Xbox a los comandos ya establecidos en el microcontrolador
# Se contempla el control de 2 motores de movimiento, 2 servomotores de torreta y 2 motores de disparo
# Manda los datos por Wi-Fi en 8 bits a la ESP32, que a su vez los reenvía a la FPGA
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA y la main.py 4.2.0 de la ESP32.
# Autor: Hafid Cruz Molina, fecha: 02/06/2026.

import socket 
import time     
import sys    
import threading
import ctypes   

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", ctypes.c_ushort),  
        ("bLeftTrigger", ctypes.c_ubyte), 
        ("bRightTrigger", ctypes.c_ubyte), 
        ("sThumbLX", ctypes.c_short),     
        ("sThumbLY", ctypes.c_short),     
        ("sThumbRX", ctypes.c_short),     
        ("sThumbRY", ctypes.c_short),     
    ]

# Estructura que envuelve los datos del control junto con el número de paquete
class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", ctypes.c_ulong), 
        ("Gamepad", XINPUT_GAMEPAD),    
    ]

# Intento de cargar la librería dinámica (DLL) de XInput en Windows
try:
    xinput = ctypes.windll.xinput1_4 
except:
    xinput = ctypes.windll.xinput1_3 

# Función para leer el estado actual del control de Xbox
def obtener_joysticks():
    state = XINPUT_STATE()
    resultado = xinput.XInputGetState(0, ctypes.byref(state))
    if resultado == 0: 
        return state.Gamepad
    return None 

# Configuración de red para apuntar al ESP32
ESP32_IP = "192.168.4.1"  
PORT = 5005       

# Creación del socket de red (IPv4, UDP)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variable global que almacena el comando actual de tracción del tanque ('S' = Stop)
estado_motor = b'S'

# Función que corre en un hilo secundario para enviar la "ráfaga" de comandos al motor
def ráfaga_motores():
    while True:
        try:
            sock.sendto(estado_motor, (ESP32_IP, PORT))
            time.sleep(0.05)
        except Exception:
            break 

# Creación e inicio del hilo en segundo plano (daemon=True cierra el hilo al cerrar el programa)
hilo_red = threading.Thread(target=ráfaga_motores, daemon=True)
hilo_red.start()

print("=== PUENTE XBOX ➔ WI-FI (TANK, TORRETAS Y L298N) ===")

# Variables para recordar la posición anterior de los servos y evitar envíos redundantes
angulo_j_previo = 127 
angulo_k_previo = 127
# Variable global para el estado inicial del Gatillo ('H' = Halt/Apagado)
estado_gatillo = b'H' 

# Función para convertir los valores brutos del joystick al formato de 1 byte de los servos
def mapear_a_grados(valor_joy):
    # Zona muerta: si el joystick está suelto (cerca del centro), fuerza el valor a 127
    if -5000 < valor_joy < 5000: 
        return 127 
    # Mapeo matemático: convierte de un rango de [-32768, 32767] a un rango de [0, 255]
    angulo = int(((valor_joy + 32768) / 65535.0) * 255)
    # Limita el valor estrictamente entre 0 y 255 para evitar errores
    return max(0, min(255, angulo))

try:
    while True:
        gamepad = obtener_joysticks()
        
        if gamepad is None:
            estado_motor = b'S'
            
            # Apagamos el mecanismo L298N por seguridad si se desconecta el control
            if estado_gatillo != b'H':
                estado_gatillo = b'H'
                sock.sendto(estado_gatillo, (ESP32_IP, PORT)) # Envía el comando de apagado al ESP32
        else:
            # ---------------------------------------------
            # 1. CONTROL DE MOTORES (JOYSTICK IZQUIERDO)
            # ---------------------------------------------
            ly = gamepad.sThumbLY
            lx = gamepad.sThumbLX
            
            # Evalúa qué dirección tomar según qué tan inclinado esté el joystick
            if ly > 15000:
                nuevo_motor = b'F'  
            elif ly < -15000:
                nuevo_motor = b'B'  
            elif lx < -15000:
                nuevo_motor = b'L'  
            elif lx > 15000:
                nuevo_motor = b'R'  
            else:
                nuevo_motor = b'S'  
                
            # Actualiza la variable global (que usa el hilo) solo si la dirección cambió
            if estado_motor != nuevo_motor:
                estado_motor = nuevo_motor
                print(f"Tanque -> {nuevo_motor.decode()}")

            # ---------------------------------------------
            # 2. CONTROL DE SERVOS (JOYSTICK DERECHO)
            # ---------------------------------------------
            ry = gamepad.sThumbRY
            rx = gamepad.sThumbRX
            
            # Pasa los valores brutos por la función de mapeo para obtener un ángulo de 0 a 255
            angulo_k_nuevo = mapear_a_grados(ry)
            angulo_j_nuevo = mapear_a_grados(rx) 
            
            # Filtro: Solo envía comando de red si el servo J se movió 2 o más grados
            if abs(angulo_j_nuevo - angulo_j_previo) >= 2:
                comando_j = f"J{angulo_j_nuevo}".encode()
                sock.sendto(comando_j, (ESP32_IP, PORT))
                angulo_j_previo = angulo_j_nuevo
                
            # Filtro: Solo envía comando de red si el servo K se movió 2 o más grados
            if abs(angulo_k_nuevo - angulo_k_previo) >= 2:
                comando_k = f"K{angulo_k_nuevo}".encode()
                sock.sendto(comando_k, (ESP32_IP, PORT))
                angulo_k_previo = angulo_k_nuevo

            # ---------------------------------------------
            # 3. CONTROL DEL GATILLO (L298N)       
            # ---------------------------------------------    
            # Lee la presión actual del gatillo derecho (valor de 0 a 255)
            rt = gamepad.bRightTrigger
            
            # Umbral de 50 (de 255) para evitar que se active con un roce accidental
            if rt > 50:
                nuevo_gatillo = b'T' # Trigger ON / Activa el puente H (L298N)
            else:
                nuevo_gatillo = b'H' # Halt / OFF / Desactiva el puente H
                
            # Si el estado del gatillo cambió entre apretado/suelto, envía la orden al ESP32
            if estado_gatillo != nuevo_gatillo:
                estado_gatillo = nuevo_gatillo
                sock.sendto(nuevo_gatillo, (ESP32_IP, PORT))
                # Imprime el estado en consola para dar feedback visual al usuario
                if nuevo_gatillo == b'T':
                    print("Gatillo Derecho -> PRESIONADO (Módulo L298N ON)")
                else:
                    print("Gatillo Derecho -> SUELTO (Módulo L298N OFF)")

        time.sleep(0.02) 

except KeyboardInterrupt:
    print("\nSistema apagado.")
