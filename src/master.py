# Versión 2.1.0
# Código del ESP32 como "maestro" de la TANG 9K.
# Se elimina la necesidad del HC-05, se cambia y flashea a Micropython y se usan nuevos comandos para el control del sistema
# Se contempla el control de 2 motores y 2 servomotores
# Recibe los datos por BLuetooth, manda 8 bits a la FPGA en formato ASCII para los servos.
# Se mejora el apartado del tiempo de espera, pasando de 5ms a 2 ms para evitar ruido eléctrico innecesario. 
# Autor: Jesús Osvaldo Yáñez Mancilla, fecha: 26/05/2026.
import machine
import bluetooth
import time
from ble_simple_peripheral import BLESimplePeripheral

# Configuración UART: TX=16 conectado al RX de la Tang Nano
uart_fpga = machine.UART(1, baudrate=9600, tx=16, rx=17)

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

servo_pendiente = None 

def on_rx(data):
    global servo_pendiente
    command = data.decode().strip().upper()
    print(f"Recibido desde App: '{command}'")
    
    # --- LÓGICA DE MOTORES ---
    if command == 'F':
        uart_fpga.write(bytes([0x01]))
        print("FPGA <- 0x01 (Adelante)")
        return
    elif command == 'B':
        uart_fpga.write(bytes([0x02]))
        print("FPGA <- 0x02 (Atrás)")
        return
    elif command == 'L':
        uart_fpga.write(bytes([0x03])) # Ahora coincide con la corrección en Verilog
        print("FPGA <- 0x03 (Izquierda)")
        return
    elif command == 'R':
        uart_fpga.write(bytes([0x04])) # Ahora coincide con la corrección en Verilog
        print("FPGA <- 0x04 (Derecha)")
        return
    elif command == 'S':
        uart_fpga.write(bytes([0x00]))
        print("FPGA <- 0x00 (Stop)")
        return

    # --- LÓGICA DE SERVOS ---
    if command == 'J':
        servo_pendiente = 'J'
        print("Modo preparado: Esperando número para Servo J...")
        return
    elif command == 'K':
        servo_pendiente = 'K'
        print("Modo preparado: Esperando número para Servo K...")
        return

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
            print(f"Error: No se pudo extraer un número válido de '{command}'")

def enviar_angulo_fpga(cabecera, angulo, nombre_servo):
    if 0 <= angulo <= 180:
        # Enviar byte de cabecera
        uart_fpga.write(bytes([cabecera]))
        
        # REDUCIDO A 2MS: Evita que la máquina de estados de la FPGA se salga de sincronía
        time.sleep_ms(2) 
        
        # Enviar byte del ángulo
        uart_fpga.write(bytes([angulo]))
        print(f"¡ENVIADO! -> FPGA <- Cabecera: {hex(cabecera)}, Ángulo: {angulo} (Servo {nombre_servo})")
    else:
        print(f"Ángulo {angulo} fuera de rango (0-180)")

print("Esperando conexión Bluetooth...")
while True:
    if sp.is_connected():
        sp.on_write(on_rx)
    time.sleep_ms(20)
