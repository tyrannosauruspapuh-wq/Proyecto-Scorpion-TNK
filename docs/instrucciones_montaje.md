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

Todo lo anterior mencionada solo fueron etapas de prueba y experimentación, siendo lo que sigue en el siguiente documento lo más relevante respecto al proyecto.

-**ACTUALIZACIÓN FPGA Y ESP32**
A continuación se muestra el diagrama final de las conexiones físicas del hardware definido, en este se aprecia la FPGA, el ESP32, los motores JGA, los servos y los respectivos puentes H.

<img width="1111" height="391" alt="image" src="https://github.com/user-attachments/assets/ffb4b7a3-14ec-4fd6-b250-ae31c81da14d" />

Considere este diagrama como referncia únicamente, ya que los pines que se definieron tanto para la ESP32 y la FPGA pueden cambiar conforme a lo que se requiera, pero la estructura es la misma en general.

Parte del ESP32 conectada a los motores de los cañones:
<img width="838" height="495" alt="image" src="https://github.com/user-attachments/assets/2bc353ae-1beb-44bb-91d6-fe86a8eafb14" />

Parte de la FPGA conectada a los puentes H, motores y seromotores:
<img width="821" height="523" alt="image" src="https://github.com/user-attachments/assets/de939dc4-eb09-46b7-9538-beb31a13c998" />

Con esto se pasaría a la otra parte importante del armado, la parte mecánica y física del propio tanque:

