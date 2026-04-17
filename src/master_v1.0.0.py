# Código del ESP32 ya siendo considerado como "maestro" del FPGA.
# Se reciben datos por bluetooth usando un HC-05, el ESP32 las procesa y envía los datos hacia la FPGA
# Para más información, revise la carpeta de docs/

from machine import Pin, UART
import time

# UART para Bluetooth 
bt = UART(1, baudrate=9600, tx=17, rx=16)

# UART para FPGA (ejemplo: conectado en GPIO4/5)
fpga = UART(2, baudrate=115200, tx=4, rx=5)

print("Listo: comandos desde Bluetooth hacía FPGA")

while True:
    if bt.any():
        cmd = bt.readline().decode().strip()
        print("Recibido BT:", cmd)

        # Validar comandos
        if cmd in ["F", "B", "L", "R", "S"]:
            # Reenviar a la FPGA
            fpga.write(cmd + "\n")
            print("Enviado a FPGA:", cmd)
        else:
            print("Comando inválido:", cmd)

    time.sleep_ms(50)
