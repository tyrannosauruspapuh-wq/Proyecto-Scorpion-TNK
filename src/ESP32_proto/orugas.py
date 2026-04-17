# Primera versión del programa para la simulación de una parte del sistema principal.
# El objetivo de este programa es simular el movimeinto de las orugas en un entorno virtual.
# Esta versión del programa esta pensada para la simuación de 4 motores DC en la plataforma de Wokwi.
# Se usan 4 botones junto con 4 LED's para la simulación de datos de entrada y respuesta del hardware.
# Para mayor información consulte la carpeta de docs/ en este mismo repositorio.

from machine import Pin
import time

# LEDs para simular las dos orugas
ledLeft = Pin(13, Pin.OUT)   # Oruga izquierda
ledRight = Pin(12, Pin.OUT)  # Oruga derecha
ledExtra1 = Pin(14, Pin.OUT) # LED para combinaciones
ledExtra2 = Pin(15, Pin.OUT) # LED para combinaciones

# Botones
btnF = Pin(25, Pin.IN, Pin.PULL_DOWN)  # Avanzar
btnB = Pin(26, Pin.IN, Pin.PULL_DOWN)  # Retroceder
btnL = Pin(27, Pin.IN, Pin.PULL_DOWN)  # Izquierda
btnR = Pin(33, Pin.IN, Pin.PULL_DOWN)  # Derecha

print("Presiona botones para simular F, B, L, R")

while True:
    # Avanzar: ambas orugas adelante
    if btnF.value():
        ledLeft.on()
        ledRight.on()
        print("Avanzar")
    else:
        ledLeft.off()
        ledRight.off()

    # Retroceder: ambas orugas atrás 
    if btnB.value():
        ledExtra1.on()
        ledExtra2.on()
        print("Retroceder")
    else:
        ledExtra1.off()
        ledExtra2.off()

    # Izquierda: solo oruga derecha activa
    if btnL.value():
        ledRight.on()
        print("Girar izquierda")
    else:
        # se apaga si no está en avanzar
        if not btnF.value():
            ledRight.off()

    # Derecha: solo oruga izquierda activa
    if btnR.value():
        ledLeft.on()
        print("Girar derecha")
    else:
        if not btnF.value():
            ledLeft.off()

    time.sleep_ms(100)
