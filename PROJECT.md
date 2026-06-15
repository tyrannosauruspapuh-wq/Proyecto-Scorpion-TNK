# TANQUE SCORPION TNK
Con su nombre inspirado en el mítico tanque de la franquicia de Halo, este proyecto tiene los siguientes objetivos generales:

- Lograr un sistema parte autonomo y parte manual, con el fin de demostrar la cohexistencia de este tipo de sistemas.
- Conseguir la creación de un modelo a escala mecanizado y con buena reistencia física ante golpes.
- Mostrar el funcionamiento más cercano a la realidad de un vehículo de combate blindado.

Todo esto dentro de un aspecto educativo y de demostración, sin incluir componentes que puedan dañar la integridad de los/las integrantes del equipo y personas relacionadas a este.

Finalmente, esto daría luz a un sistema que muestre de manera realista el funcionamiento de un equipo ya conocido en la industria militar, permitiendo asi el acercamiento a un entorno más real y comprensivo de las tecnologías que sí se usan en el día a día en las grandes industrias, no solo militarmente hablando, sino también en términos de creación y desarrollo tanto mecánico, de hardware y software, como se ha específicado anteriormente.

# Lista de componentes a utilizar
### Se planea el uso de:
- 1 microcontrolador ESP32
- 1 FPGA Tang NANO 9K
- 1 Control de XBOX
- 2 Motores DC de caja reductora
- 2 Motores DC JGA25-370
- 2 Servomotores SG90
- 2 Puentes H TB6612FNG
- 1 Puente H L298N
- 1 Sensor ultrasónico
- 4 baterías 4.4V 3300 mAh
- 8 Baterías 1.2V 1300 mAh
- Estrellas de piñones de bicicleta
- Cadenas de bicicleta para las orugas
- Triplay
- Solera de 1/2" para el chasis interno
- Ángulo de 2"
- Lámina calibre 21 para la carrocería
- Tubos de plástico para los cañones
- Hojas de papel
- PlastiLoka
- Herramienta necesaria para el manejo de los materiales (pulidora, cortadora, esmeril, extractor de cadenas, taladro).

# Cronograma de trabajo
- **Fase 1: Cimentación y Definición (9 de marzo al 29 de marzo):** Se realizará la investigación de Hardware para definir el FPGA y los puentes H a utilizar. Se hará el diseño preliminar del chasis asi como sus planos, de igual forma, se realizarán pruebas individuales de los motores de caja reductora y servomotores con el ESP32.
- **Fase 2: Desarrollo Modular (30 de marzo al 26 de abril):** Se hará la programación de la lógica de control y recepción de señales del sensor ultrasónico con el ESP32, también se hará el desarrollo en Verilog para el control de movimiento y la gestión de señales para reducir el ruido eléctrico. Se hará ensamblaje del chasis y montaje de la estructura interna resistente a impactos. 
- **Fase 3: Integración y Comunicación (27 de abril al 17 de mayo):** Se establecerá la comunicación fiable entre el ESP32 y el FPGA. SE hará la configuración del banco de baterías (4.4V y 2V) para separar la etapa de potencia y de control. Se realizarán las primeras pruebas de campo, movimiento del tanque y respuesta de los servos de la torreta.
- **Fase 4: Optimización y Pruebas Finales (18 de mayo al 31 de mayo):** Se refinará la fluidez de los movimientos y la respuesta del sensor, así como ajustes finales en el hardware para garantizar la autonomía y la estabilidad. Se hará la documentación final, actualizando el README, el manual de usuario y los roles desempeñados por el equipo.
- **Fase 5: Presentación y Cierre (1 de junio al 15 de junio):** Presentación del prototipo funcionando de manera realista y cierre de las materias de Programación Avanzada y Sistemas Digitales. 
