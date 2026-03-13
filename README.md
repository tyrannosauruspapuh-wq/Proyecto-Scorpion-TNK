# Proyecto-Scorpion-TNK
# Repositorio dedicado al proyecto integrador de las materias de Programacion avanzada y Sistemas digitales
### Como objetivo general se busca la mejora de un sistema ya creado que simula a un carro-tanque del siglo pasado
### Para esto, se busca la creacion de un nuevo sistema modular similar a los tanques blindados de hoy en día, que simule de forma segura cada funcion que estos tienen, de igual forma, se busca la implementación de nuevos sistemas y tecnologías no implementadas antes en el primer prototipo que permitan darle al proyecto autonomia en el aspecto de hardware, eliminando asi problemas como lo es el ruido eléctrico en ciertos componentes y una mejor fluidez en cada movimiento que este haga.

### Se diseñaría un prototipo basado en uno anteriormente hecho, que mezcle 3 característicaas principales, siendo el diseño mecánico, la integración de software mediante un microcontrolador y de hardware, implementado por un FPGA o en su defecto un CPLD.

### Todo esto dentro de un aspecto educativo y de demostración, sin incluir componentes que puedan dañar la integridad de los/las integrantes del equipo y personas relacionadas a este.

### Finalmente, todo esto daría luz a un sistema que muestre de manera realista el funcionamiento de un equipo ya conocido en la industria militar, permitiendo asi el acercamiento a un entorno más real y comprensivo de las tecnologías que sí se usan en el día a día en las grandes industrias, no solo militarmente hablando, sino también en términos de creación y desarrollo tanto mecánico, de hardware y software, como se ha específicado anteriormente.

# Lista de componentes a utilizar
### Se planea el uso de:
### 1 microcontrolador ESP32
### 1 FPGA (Aún por discutir)
### 5 Motores de caja reductora (Aún por discutir)
### 2 Servomotores (El modelo específico aún se encuentra en discusión)
### 2 Puentes H L298N (Aún por discutir)
### 1 Sensor ultrasónico
### 2 baterías 4.4V 3300 mAh
### 4 Baterías 2V 1300 mAh
### Posible uso de madera ligera para el chasis del vehpiculo
### Partes mecánicas para las orugas y ruedas del mismo
### Estructura interna hecha de madera u otro material resistente a impactos

# Diagrama de conexión entre componentes electrónicos
### A continuación se presenta un diagrama básico de las conexiones entre un microcontrolador y los 5 motores así como ambos servos, cabe aclarar que aún no se tiene previsto el modelo de FPGA a usar y por ende, no se tiene un diagrama de conexión entre el microcontrolador y la placa de FPGA que sea fiable para el proyecto.
### De igual forma, se puede ver el uso de un Arduino UNO en la placa, esto es, para fines prácticos, gracias a la similitud entre el UNO y el ESP32 es posible guiarse por este diagrama de conexión.
<img width="1385" height="719" alt="Captura de pantalla 2026-03-13 135301" src="https://github.com/user-attachments/assets/e712ba2d-d547-4c2c-9328-c7d7df3142d7" />

