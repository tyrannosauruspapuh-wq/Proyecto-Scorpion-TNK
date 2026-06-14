// Versión 1.2.0 del módulo top para la Tang Nano 9K
// Control de 2 Servos y 2 motores, datos enviados por UART desde el ESP32 en formato de 8 bits, correción del código en el apartado de UART
// Mejora de filtrado de ruido eléctrico.
// Autor Jesús Osvaldo Yáñez Mancilla, fecha: 26/05/2026
module tank_controller (
    input clk,            // 27MHz nativos de la Tang Nano 9K
    input rx,             // Línea proveniente del TX del ESP32
    output reg [3:0] motors = 4'b0000, // Inicializado apagado
    output pwm_j,         
    output pwm_k          
);

parameter CLK_FREQ = 27000000;
parameter BAUD_RATE = 9600;
parameter [16:0] WAIT_TIME = CLK_FREQ / BAUD_RATE; // 2812 ciclos exactos por bit

// --- TRIPLE ETAPA DE SINCRONIZACIÓN CONTRA METAESTABILIDAD ---
// Reemplazamos la etapa simple por una triple para blindar la señal contra chispas de motores
reg rx_stage1, rx_stage2, rx_sync;
always @(posedge clk) begin
    rx_stage1 <= rx;
    rx_stage2 <= rx_stage1;
    rx_sync   <= rx_stage2;

end
    
reg [16:0] count = 17'd0;
reg [3:0] bit_idx = 4'd0;
reg [7:0] data_raw = 8'd0;
reg receiving = 1'b0;
reg [1:0] state_mode = 2'd0; 



// Registros estables de salida hacia los módulos PWM
reg [7:0] angulo_j = 8'd90; 
reg [7:0] angulo_k = 8'd90;



// --- LÓGICA RECEPTOR UART RECALIBRADA ---
always @(posedge clk) begin
    if (!receiving && rx_sync == 1'b0) begin
        receiving <= 1'b1;
        count     <= (WAIT_TIME / 2) - 1; // Muestreo exacto a la mitad del bit de START
        bit_idx   <= 4'd0;
    end else if (receiving) begin

        // CORRECCIÓN CRUCIAL: WAIT_TIME - 1 para garantizar un divisor exacto de ciclos
     if (count < WAIT_TIME - 1) begin
            count <= count + 17'd1;
        end else begin
            count <= 17'd0; // Resetear contador de ciclos de manera síncrona
            if (bit_idx < 4'd8) begin
                // Muestreo limpio en el centro exacto de cada bit de datos
                data_raw[bit_idx] <= rx_sync;
                bit_idx <= bit_idx + 4'd1;
            end else if (bit_idx == 4'd8) begin

                // Esperar el periodo completo del STOP BIT (línea en alto) para dar estabilidad
                bit_idx <= bit_idx + 4'd1;
            end else begin


                // ¡Final del ciclo de parada de forma segura!
                receiving <= 1'b0; 
                bit_idx   <= 4'd0; 



// --- PROCESAMIENTO CON FILTRO DE SEGURIDAD ---
if (state_mode == 2'd1) begin
// Filtro anti-ruido: Solo actualiza el servo si el dato está en un rango real (0 a 180)
if (data_raw <= 8'd180) begin
angulo_j <= data_raw;
end

state_mode <= 2'd0; // Regresa al modo comando obligatoriamente
end else if (state_mode == 2'd2) begin

// Filtro anti-ruido
 if (data_raw <= 8'd180) begin
angulo_k <= data_raw;
end
state_mode <= 2'd0; // Regresa al modo comando obligatoriamente
 end else begin
 case (data_raw)

                        8'h01: motors <= 4'b1010; // Adelante (F)
                        8'h02: motors <= 4'b0101; // Atrás (B)
                        8'h03: motors <= 4'b1001; // Derecha (R)
                        8'h04: motors <= 4'b0110; // Izquierda (L)
                        8'h00: motors <= 4'b0000; // Parar (S)
                        8'hAA: state_mode <= 2'd1; // Cabecera Servo J
                        8'hBB: state_mode <= 2'd2; // Cabecera Servo K
                        default: motors <= motors; // Ignorar cualquier ruido serial basura

                    endcase

                end

            end

        end

    end

end


// --- INSTANCIACIÓN DE MÓDULOS PWM ---
servo_pwm control_j (
    .clk(clk),
    .angle(angulo_j),
    .pwm_out(pwm_j)
);
servo_pwm control_k (
    .clk(clk),
    .angle(angulo_k),
    .pwm_out(pwm_k)
);

endmodule
// --- MÓDULO AUXILIAR PWM CALIBRADO A 27MHz ---

module servo_pwm (
    input clk,
    input [7:0] angle,
    output reg pwm_out

);

    reg [19:0] counter = 20'd0;

    reg [19:0] duty_cycle;

    always @(posedge clk) begin

        if (angle <= 8'd180) begin

            duty_cycle <= 20'd27000 + ({12'd0, angle} * 20'd150); 
        end else begin
            duty_cycle <= 20'd54000; // Límite de seguridad para 180 grados
        end

        // Periodo total de 20 ms para el servo = 540,000 ciclos de reloj - 1
        if (counter < 20'd540000 - 1) 
            counter <= counter + 20'd1;
        else 
            counter <= 20'd0;

        // Salida limpia
        pwm_out <= (counter < duty_cycle);
    end
endmodule
