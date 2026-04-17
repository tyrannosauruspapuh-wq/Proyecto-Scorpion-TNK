# Primera versión del programa para la simulación de la segunda parte del sistema principal.
# El objetivo de este programa es simular el movimiento de la torreta y cañón en un entorno virtual.
# Esta versión del programa esta pensada para la simuación de 2 Servomotores en la plataforma de Wokwi.
# Se usan 4 botones junto con 2 Servos para la simulación de movimiento, usando los datos de entrada y respuesta del hardware.
# Para mayor información consulte la carpeta de docs/ en este mismo repositorio.

from machine import Pin, PWM
import time

# Pines de los servos
servoCanon = PWM(Pin(5), freq=50)     # Servo cañón
servoTorreta = PWM(Pin(4), freq=50)   # Servo torreta

# Botones
btnCanonUp = Pin(32, Pin.IN, Pin.PULL_DOWN)   # Subir cañón
btnCanonDown = Pin(33, Pin.IN, Pin.PULL_DOWN) # Bajar cañón
btnTorretaLeft = Pin(26, Pin.IN, Pin.PULL_DOWN) # Girar izquierda
btnTorretaRight = Pin(27, Pin.IN, Pin.PULL_DOWN) # Girar derecha

# Posiciones iniciales
canonPos = 90
torretaPos = 90

def angle_to_duty(angle):
    # Mapear ángulo (0-180) a duty (0-65535)
    return int((angle/180*2+0.5) * 65535/20)

print("Control de cañón y torreta con botones")

while True:
    # Control cañón
    if btnCanonUp.value() and canonPos < 180:
        canonPos += 5
        servoCanon.duty_u16(angle_to_duty(canonPos))
        print("Cañón arriba:", canonPos)
        time.sleep_ms(200)
    elif btnCanonDown.value() and canonPos > 0:
        canonPos -= 5
        servoCanon.duty_u16(angle_to_duty(canonPos))
        print("Cañón abajo:", canonPos)
        time.sleep_ms(200)

    # Control torreta
    if btnTorretaLeft.value() and torretaPos > 0:
        torretaPos -= 5
        servoTorreta.duty_u16(angle_to_duty(torretaPos))
        print("Torreta izquierda:", torretaPos)
        time.sleep_ms(200)
    elif btnTorretaRight.value() and torretaPos < 180:
        torretaPos += 5
        servoTorreta.duty_u16(angle_to_duty(torretaPos))
        print("Torreta derecha:", torretaPos)
        time.sleep_ms(200)
