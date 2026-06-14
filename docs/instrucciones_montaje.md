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

-**ARMADO FÍSICO DEL TANQUE USANDO DIVERSIDAD DE MATERIALES**

1.- Primero, se hace una base que sostenga a todo el tanque y su posterior carrocería, usando planos de referencia para su creación:
<img width="1201" height="1600" alt="1417d302-6e38-4ea7-a0de-0bdcfd13d8ee" src="https://github.com/user-attachments/assets/5975f787-ead4-487e-ae1a-60bbb9d41971" />

 2.- Después se nivelo dicha base usando pasta automotriz, aunque puede utilizarse otro material, asimismo, usando una bse genérica de un carro arduino, se  unió a esta para dar una base que permita colocar todo el hardware programable:
 <img width="1201" height="1600" alt="3ef3bc10-fbf4-49aa-8698-52282a767a99" src="https://github.com/user-attachments/assets/fba123c1-1fa8-4342-b00e-4aaf40fbeb0c" />

<img width="1201" height="1600" alt="7d1d7147-b17d-4b73-86fd-cef1ee6dd3f0" src="https://github.com/user-attachments/assets/d141a6f3-630a-44b1-9970-68860bca24e9" />

3.- Posteriormente se buscaron piezas clave de bicicleta, como lo son estrellas de distinto tamaño para su uso en las orugas, asimismo, se usaron cadenas de este mismo tipo:
<img width="1201" height="1600" alt="8df9058c-5218-49c5-860c-aae2d71eb21e" src="https://github.com/user-attachments/assets/41215144-2da9-4fb5-adae-8f1af9bee3da" />

4.- Luego, usando 2 piezas de ángulo, se atornillan en la base principal para darle forma a los ejes de las orugas posteriores:
<img width="1201" height="1600" alt="298161c2-caa8-49a7-9447-f4bb337d0d70" src="https://github.com/user-attachments/assets/36440958-d54d-413c-8c0f-286573d682b6" />

<img width="1201" height="1600" alt="ea37894c-5c79-4199-babc-8a21dc9a7032" src="https://github.com/user-attachments/assets/7cfcf3e4-e595-4bc8-ac5c-fd724c48ecd9" />

5.- De igual forma, se biscaron piezas personalizadas para poder ir terminando el aspecto del chasis, dando lugar a lo que sería la guía frontal del tanque:
<img width="1600" height="1201" alt="4c6f92ee-dfe6-48f0-a545-9758d876c4b8" src="https://github.com/user-attachments/assets/4e95f027-2293-43d0-aae6-2bfda7a90fd4" />

6.- Ahora pasamos a la parte de la carrocería, usando lámina calibre 21, se empezó a dar forma tanto para las partes laterales y frontales del taqnue:
<img width="1201" height="1600" alt="3d3189bb-d9b5-4c2d-9f95-27fd55bdb429" src="https://github.com/user-attachments/assets/61706674-19a3-4957-aeb4-628437bc0a3b" />

7.- Se hace una prueba piloto para verificar que todo este alineado:
<img width="1201" height="1600" alt="3b06a67a-c0cd-40f3-8e3a-d7f6ba292b4c" src="https://github.com/user-attachments/assets/260a1781-b7da-4ac6-897a-f6d87161769a" />

<img width="1201" height="1600" alt="f19d294e-035b-486d-aeeb-c9a6fb3fd334" src="https://github.com/user-attachments/assets/39b2be34-a637-4069-bffb-ed04ae5a4ed3" />

8.- Ahora regresamos a la parte del hardware programable, siguiendo la guía ya presentada anteriormente, se hacen las conexiones correspondientes, primero usando un LN298 como primer intento:
<img width="1600" height="1201" alt="0a5ab479-9f1f-479f-8151-16891cb53cc3" src="https://github.com/user-attachments/assets/b8260ee9-5808-4515-ad78-c176912d1b0a" />

9.- Después de concluir con el LN298, se pasa a usar el puente H definitivo:
<img width="1201" height="1600" alt="9c5ee523-f759-4761-af7b-2fd33a784205" src="https://github.com/user-attachments/assets/6c203612-4fbd-4368-a6f3-e52a26d8b778" />

10.- Se cambian también los motores antiguos por los nuevos:
<img width="1201" height="1600" alt="9c5ee523-f759-4761-af7b-2fd33a784205" src="https://github.com/user-attachments/assets/bebb9505-82d4-4826-99be-7a7ce8e653d5" />

<img width="1600" height="1201" alt="7f2e09f2-5e7f-436c-9102-7d96073bad98" src="https://github.com/user-attachments/assets/7e4eff61-7f24-4200-b315-453b2a33a3ac" />

11.- Se cambia el acrílico por triplay debido a su mayor resistencia:
<img width="1201" height="1600" alt="8d8c1e1d-282d-41e6-b5f1-f2e5c84eb635" src="https://github.com/user-attachments/assets/e8fe8718-ed5c-4aa1-a327-ca48dd04f5f6" />

12.- Siguiendo con el chasis, se colocan las estrellas a los motores y al mismo tiemmpo, se le hace una base para que puedan acoplarse a la base principal, de igual forma, se empieza a medir la cadena:
<img width="1201" height="1600" alt="08463447-e29d-40fd-9e20-4567043215e7" src="https://github.com/user-attachments/assets/db673257-2164-4653-bc24-ea1e6f11c9d6" />

13.- Se colocan las demas estrellas:
<img width="1600" height="1201" alt="fa5e8927-0a41-4888-99ef-7130eb0903b3" src="https://github.com/user-attachments/assets/92e37227-1cd8-479e-82d6-099eabb80569" />

<img width="1201" height="1600" alt="ad86d10b-e0a8-4ea7-b131-75078260a663" src="https://github.com/user-attachments/assets/dcdf5286-9f0d-453f-88a5-3c71f1b6c328" />

14.- Se colocan las demás partes del chasis para las orugas:
<img width="1201" height="1600" alt="b69180a1-146f-4750-80ef-069ce976716e" src="https://github.com/user-attachments/assets/c4b4e142-07c6-41aa-a688-1e0cf8b42ddc" />

<img width="1600" height="1201" alt="07d1bf81-0daa-45b4-b102-aee51aafeeed" src="https://github.com/user-attachments/assets/d6be9cbe-61ab-4361-83b6-2aebaa17ed55" />

15.- Se coloca la parte del hardware programable al chasis para corroborar su funcionamiento:
<img width="1201" height="1600" alt="d0ece6af-b7d5-4650-b4f7-11222889533d" src="https://github.com/user-attachments/assets/ca1872b8-438e-4c53-89e6-65097137c60d" />

<img width="1600" height="1201" alt="e3a910d0-6768-48ff-8f9c-f7c476fd97c0" src="https://github.com/user-attachments/assets/371d1960-6bfc-4276-a625-1295e118a5d4" />

16.- Se colocan las orugas del tanque ya medidas, asimismo se ponen guías para las orugas:
<img width="1201" height="1600" alt="554e7f53-6f77-4ff8-9187-cc25bc8bd3f7" src="https://github.com/user-attachments/assets/b94705c4-9b85-4034-8f0d-4e7cbea6d3e2" />

17.- Para la parte del cañón, se uso el siguiente video como base para el funcionamiento, hasta el minuto 3.47 como relevante para esta parte:
https://www.youtube.com/watch?v=IIAEeSaI-Mk

18.- Usando cuñas y tornillos para fijar la carrocería, se coloca finalmente así como el cañon y lo demás correspondiente:
<img width="1600" height="1201" alt="ad1a870f-d3a3-49c8-871e-51a47ba1b458" src="https://github.com/user-attachments/assets/875dbbd9-e321-4abf-92ee-49f8b100a686" />

19.- Se coloca decoración referente al equipo responsable del proyecto y, listo!!!, tenemos un tanque funcional con un control de xbox:

<img width="1600" height="1201" alt="01d969dd-3010-43b6-bd10-515d4d23ddc3" src="https://github.com/user-attachments/assets/5e929522-0d52-4a7a-9565-d5ecea563f2f" />

<img width="1201" height="1600" alt="3e142e67-ebde-41a0-86a6-a4a1a06d621e" src="https://github.com/user-attachments/assets/2eccbb12-2ae5-4804-af59-3e5785c49dd2" />
