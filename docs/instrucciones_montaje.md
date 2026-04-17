- 13 de marzo del 2026
# Diagrama de conexión entre componentes electrónicos
A continuación se presenta un diagrama básico de las conexiones entre un microcontrolador y los 5 motores así como ambos servos, cabe aclarar que aún no se tiene previsto el modelo de FPGA a usar y por ende, no se tiene un diagrama de conexión entre el microcontrolador y la placa de FPGA que sea fiable para el proyecto.

De igual forma, se puede ver el uso de un Arduino UNO en la placa, esto es, para fines prácticos, gracias a la similitud entre el UNO y el ESP32 es posible guiarse por este diagrama de conexión.
<img width="1385" height="719" alt="Captura de pantalla 2026-03-13 135301" src="https://github.com/user-attachments/assets/e712ba2d-d547-4c2c-9328-c7d7df3142d7" />

Conforme se avance en el proyecto se irán agregando las fotos del hardware en físico así como sus instrucciones correspondientes.

- Actualización 17 de abril del 2026:

# Diagrama de conexión en la plataforma de wokwi
## Orugas:
Aquí se ve el diagrama de conexión para el código prototipo de orugas.py, se usaron botones para simular las señales recibidas por medio de Bluetooth:

Se usan 4 botones para cada comando, siendo Foward, Back, Left y Right, el sistema cada que deja de recibir la señal vuelve al estado Stop.
 <img width="914" height="633" alt="Captura de pantalla 2026-04-17 145129" src="https://github.com/user-attachments/assets/4eec82f3-f495-418a-bf5e-5dd66fe7ff74" />

Se puede encontrar dicho proyecto en Wokwi en el siguiente enlace: 
https://wokwi.com/projects/461515831621372929

## Torreta y cañon (movimiento):
Aquí se aprecia el diagrama de conexión para el código prototipo de torretas.py, se usaron botones para simular los comando recibidos por medio de Bluetooth

Se usan 2 botnes para el servo correspondiente del giro de izquierda a derecha, asimismo, los otros 2 botones son usados para el movimiento de arriba y abajo, modificando el angulo de disparo del sistema.
<img width="893" height="623" alt="Captura de pantalla 2026-04-17 150105" src="https://github.com/user-attachments/assets/e7bdd3c8-0ed9-4183-a313-04b180590f5d" />

Se puede encontrar dicho proyecto en Wokwi en el siguiente enlace:
https://wokwi.com/projects/461534388883186689
