La verificación de este proyecto representó el reto más grande, principalmente debido a la transición del mundo digital al mundo físico. En la etapa inicial, 
trabajamos en un entorno controlado, validando la máquina de estados de la UART mediante bancos de prueba (Testbench). Estos bancos simulaban ráfagas ideales de bits, 
lo que nos permitió confirmar que la lógica de transmisión y recepción funcionaba correctamente bajo condiciones teóricas. Sin embargo, al trasladar el diseño a la placa física, 
nos encontramos con un escenario completamente distinto: los motores no respondían a las órdenes enviadas, lo que evidenció que las condiciones reales introducían variables que no estaban contempladas en la simulación.

Para abordar este problema, aplicamos un proceso sistemático de diagnóstico por aislamiento. En primer lugar, aislamos 
la etapa de potencia y verificamos cuidadosamente las conexiones de tierra. Con el multímetro comprobamos que existiera una referencia 
común entre el módulo de comunicación, la batería de los motores y la FPGA MAX II. Fue en este punto donde descubrimos un error crítico: sin una masa compartida, la UART 
interpretaba únicamente ruido eléctrico, generando lecturas erróneas y provocando que los motores permanecieran inactivos. 
Esta corrección fue fundamental para establecer una base sólida de comunicación entre los módulos.

Posteriormente, nos enfocamos en la capa de software y en la interacción con la aplicación móvil. Realizamos pruebas exhaustivas monitoreando los bytes transmitidos en 
la consola serie, asegurándonos de que los identificadores asignados a cada servo estuvieran correctamente sincronizados con las órdenes enviadas desde 
la interfaz gráfica. Este paso permitió confirmar que la lógica de direccionamiento funcionaba y que los comandos llegaban íntegros al sistema, eliminando la posibilidad de errores por desajustes en la codificación.

Finalmente, abordamos la calibración del sensor ultrasónico en tiempo real. Este componente, sensible a la frecuencia de oscilación, requería ajustes 
finos en los contadores implementados en Verilog. Adaptamos dichos contadores para que coincidieran con la frecuencia real del chip de Altera, garantizando que las 
mediciones de distancia fueran precisas y estables. Este proceso de calibración no solo mejoró la confiabilidad del sistema, 
sino que también permitió integrar el sensor como parte esencial del control de los motores, cerrando el ciclo de verificación entre hardware y software.

De esta manera, la verificación no se limitó a confirmar la lógica digital, sino que implicó un trabajo integral de diagnóstico eléctrico, sincronización de comunicación y calibración de sensores, 
lo que nos permitió superar las limitaciones iniciales y consolidar el funcionamiento del proyecto en condiciones reales.
