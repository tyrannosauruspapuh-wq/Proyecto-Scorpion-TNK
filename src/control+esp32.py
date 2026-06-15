# Versión 1.1.0
# Script de Python que corre en una PC conectada por Wi-Fi al ESP32, donde se traducen los comandos del control de Xbox a los comandos ya establecidos en el microcontrolador
# Se contempla el control de 2 motores y 2 servomotores
# Manda los datos por Wi-Fi en 8 bits a la ESP32, que a su vez los reenvía a la FPGA
# Se mantiene la traducción de los datos y el posterior envio UART a la FPGA.
# Versión estable con la top.v 3.0.0 de la FPGA y la main.py 4.1.0 de la ESP32.
# Autor: Hafid Cruz Molina, fecha: 01/06/2026.

import socket   
import time
import sys  
import threading
import ctypes   

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", ctypes.c_ushort),      # Estado de los botones (A, B, X, Y, etc.)
        ("bLeftTrigger", ctypes.c_ubyte),   # Eje del gatillo izquierdo (0 a 255)
        ("bRightTrigger", ctypes.c_ubyte),  # Eje del gatillo derecho (0 a 255)
        ("sThumbLX", ctypes.c_short),       # Eje X del joystick izquierdo (Izquierda/Derecha)
        ("sThumbLY", ctypes.c_short),       # Eje Y del joystick izquierdo (Arriba/Abajo)
        ("sThumbRX", ctypes.c_short),       # Eje X del joystick derecho (Izquierda/Derecha)
        ("sThumbRY", ctypes.c_short),       # Eje Y del joystick derecho (Arriba/Abajo)
    ]

# Estructura para el estado general del control
class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", ctypes.c_ulong), 
        ("Gamepad", XINPUT_GAMEPAD),  
    ]

try:
    xinput = ctypes.windll.xinput1_4 
except:
    xinput = ctypes.windll.xinput1_3

def obtener_joysticks():
    state = XINPUT_STATE()
    resultado = xinput.XInputGetState(0, ctypes.byref(state))
    if resultado == 0:
        return state.Gamepad 
    return None

ESP32_IP = "192.168.4.1"  
PORT = 5005        

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

estado_motor = b'S'

def ráfaga_motores():
    while True:
        try:
            sock.sendto(estado_motor, (ESP32_IP, PORT))
            time.sleep(0.05) 
        except Exception:
            break

hilo_red = threading.Thread(target=ráfaga_motores, daemon=True)
hilo_red.start()

print("=== PUENTE XBOX ➔ WI-FI (TANK, TORRETAS Y L298N) ===")

# Variables para recordar la posición anterior de los servos (inician en el centro: 127)
angulo_j_previo = 127 
angulo_k_previo = 127

# Función para convertir los valores del joystick (-32768 a 32767) al formato de los servos (0 a 255)
def mapear_a_grados(valor_joy):
    # Zona muerta: si el joystick está casi en el centro (-5000 a 5000), se fuerza al centro perfecto (127)
    if -5000 < valor_joy < 5000: 
        return 127 
    # Ecuación matemática para escalar el valor del rango del joystick al rango de 0-255
    angulo = int(((valor_joy + 32768) / 65535.0) * 255)
    # Se asegura de que el resultado nunca sea menor a 0 ni mayor a 255
    return max(0, min(255, angulo))

try:
    while True:
        # Lee el control en cada ciclo
        gamepad = obtener_joysticks()
        
        if gamepad is None:
            estado_motor = b'S' # Por seguridad, detiene el tanque si se desconecta el control
            
        else:
            # ---------------------------------------------
            # 1. CONTROL DE MOTORES (JOYSTICK IZQUIERDO)
            # ---------------------------------------------
            ly = gamepad.sThumbLY
            lx = gamepad.sThumbLX
            
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
                
            if estado_motor != nuevo_motor:
                estado_motor = nuevo_motor
                print(f"Tanque -> {nuevo_motor.decode()}")

            # ---------------------------------------------
            # 2. CONTROL DE SERVOS (JOYSTICK DERECHO)
            # ---------------------------------------------
            ry = gamepad.sThumbRY
            rx = gamepad.sThumbRX
            
            # Calcula los nuevos ángulos para la torreta llamando a la función de mapeo
            angulo_k_nuevo = mapear_a_grados(ry) # Eje Y controla el servo K 
            angulo_j_nuevo = mapear_a_grados(rx) # Eje X controla el servo J
            
            # Solo envía el comando del servo J si el ángulo cambió en al menos 2 grados
            if abs(angulo_j_nuevo - angulo_j_previo) >= 2:
                comando_j = f"J{angulo_j_nuevo}".encode() # Crea la cadena, ej: "J180" y la pasa a bytes
                sock.sendto(comando_j, (ESP32_IP, PORT))  # La envía directamente por UDP
                angulo_j_previo = angulo_j_nuevo          # Actualiza el registro de la posición
                
            # Solo envía el comando del servo K si el ángulo cambió en al menos 2 grados
            if abs(angulo_k_nuevo - angulo_k_previo) >= 2:
                comando_k = f"K{angulo_k_nuevo}".encode() # Crea la cadena, ej: "K90" y la pasa a bytes
                sock.sendto(comando_k, (ESP32_IP, PORT))  # La envía directamente por UDP
                angulo_k_previo = angulo_k_nuevo          # Actualiza el registro de la posición

        time.sleep(0.02) 

except KeyboardInterrupt:
    print("\nSistema apagado.")
