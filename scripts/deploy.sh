Flasheo del ESP32 con micropython
01
Instalar dependencias para ESP32
Necesitas tener Python y esptool para flashear el firmware.
Instala Python 3.x en tu PC
Abre terminal y ejecuta: pip install esptool
Conecta el ESP32 por USB y verifica el puerto COM asignado

02
Descargar firmware MicroPython
Obtén la versión oficial de MicroPython para ESP32.
Ve a micropython.org/download
Descarga el archivo .bin más reciente para ESP32

03
Flashear ESP32 con esptool
Usa esptool para borrar y grabar el firmware.
Borrar flash: esptool.py --chip esp32 erase_flash
Grabar firmware: esptool.py --chip esp32 --port COMx write_flash -z 0x1000 firmware.bin
Sustituye COMx por el puerto correcto

04
Probar MicroPython en ESP32
Verifica que el firmware funciona.
Abre Thonny IDE
Selecciona MicroPython (ESP32) como intérprete
Ejecuta un script simple: print("Hola ESP32")


Flashear FPGA Tang Nano 9K
01
Instalar Gowin IDE
Descarga e instala el entorno para FPGA.
Ve a la página oficial de Gowin Semiconductor
Descarga Gowin IDE compatible con tu sistema operativo
Instala los drivers USB/JTAG incluidos

02
Preparar proyecto FPGA
Crea tu proyecto y compila el código Verilog.
Abre Gowin IDE y crea un nuevo proyecto
Importa tu código Verilog/VHDL
Ejecuta Synthesis → Place & Route → Generate Bitstream

03
Flashear FPGA
Carga el bitstream en la Tang Nano/FPGA.
Conecta la FPGA por USB
En Gowin IDE, abre Programmer Tool
Selecciona el archivo .fs o .bin generado
Haz clic en Program para flashear
