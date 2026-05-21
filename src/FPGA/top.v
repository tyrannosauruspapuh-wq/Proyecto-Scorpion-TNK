// Versión 1.0.0 del módulo top para la Tang Nano 9K
// Control de 2 Servos y 2 motores, datos enviados por UART desde el ESP32 en formato de 8 bits
// Autor Jesús Osvaldo Yáñez Mancilla, fecha: 21/05/2026
module tank_controller (
    input clk,            // 27MHz
    input rx,             
    output reg [3:0] motors = 4'b0000, // Inicializado a 0 por defecto al encender
    output pwm_j,         
    output pwm_k          
);

parameter CLK_FREQ = 27000000;
parameter BAUD_RATE = 9600;
parameter [16:0] WAIT_TIME = CLK_FREQ / BAUD_RATE; // Forzado a 17 bits para emparejar

// --- REGISTROS INTERNOS ---
reg rx_sync;
always @(posedge clk) rx_sync <= rx;

reg [16:0] count = 17'd0;
reg [3:0] bit_idx = 4'd0;
reg [7:0] data_raw = 8'd0;
reg receiving = 1'b0;
reg [1:0] state_mode = 2'd0; 

// Registros estables de salida hacia los módulos PWM
reg [7:0] angulo_j = 8'd90; 
reg [7:0] angulo_k = 8'd90;

// Registros búfer intermedios para blindaje CDC (Clock Domain Crossing)
reg [7:0] angulo_j_buf = 8'd90;
reg [7:0] angulo_k_buf = 8'd90;

// --- LÓGICA RECEPTOR UART ---
always @(posedge clk) begin
    if (!receiving && rx_sync == 1'b0) begin
        receiving <= 1'b1;
        count <= (WAIT_TIME / 2); // Muestreo en la mitad del bit de START
        bit_idx <= 4'd0;
    end else if (receiving) begin
        if (count < WAIT_TIME) begin
            count <= count + 17'd1;
        end else begin
            count <= 17'd0; // Resetear contador para el siguiente bit
            
            if (bit_idx < 4'd8) begin
                // Muestreo de los 8 bits de datos (0 al 7)
                data_raw[bit_idx] <= rx_sync;
                bit_idx <= bit_idx + 4'd1;
            end else if (bit_idx == 4'd8) begin
                // --- ESPERAR UN BIT MÁS (STOP BIT) ---
                // Esto le da tiempo físico a 'data_raw' de estar 100% listo y estable en los registros
                bit_idx <= bit_idx + 4'd1;
            end else begin
                // ¡bit_idx == 9! El Stop bit ha terminado y data_raw está perfectamente asentado
                receiving <= 1'b0; 
                bit_idx <= 4'd0; 

                // Ahora procesamos con total estabilidad de registros utilizando búferes intermedios
                if (state_mode == 2'd1) begin
                    angulo_j_buf <= data_raw;
                    angulo_j     <= data_raw; // Transferencia segura en un solo ciclo de reloj
                    state_mode   <= 2'd0;     // Forzar regreso seguro al modo normal
                end else if (state_mode == 2'd2) begin
                    angulo_k_buf <= data_raw;
                    angulo_k     <= data_raw; // Transferencia segura en un solo ciclo de reloj
                    state_mode   <= 2'd0;     // Forzar regreso seguro al modo normal
                end else begin
                    case (data_raw)
                        8'h01: motors <= 4'b1010; // Adelante (F)
                        8'h02: motors <= 4'b0101; // Atrás (B)
                        8'h03: motors <= 4'b1001; // Derecha (R)
                        8'h04: motors <= 4'b0110; // Izquierda (L)
                        8'h00: motors <= 4'b0000; // Parar (S)
                        8'hAA: begin
                            state_mode <= 2'd1;   // Esperar ángulo Servo J
                        end
                        8'hBB: begin
                            state_mode <= 2'd2;   // Esperar ángulo Servo K
                        end
                        default: motors <= motors; // Mantener estado actual
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


// --- MÓDULO AUXILIAR PWM RECALIBRADO ---
module servo_pwm (
    input clk,
    input [7:0] angle,
    output reg pwm_out
);
    reg [19:0] counter = 20'd0;
    reg [19:0] duty_cycle;

    // Forzamos que la operación aritmética completa se evalúe en formato de 20 bits
    always @(posedge clk) begin
        if (angle <= 8'd180) begin
            duty_cycle <= 20'd27000 + ({12'd0, angle} * 20'd150); 
        end else begin
            duty_cycle <= 20'd54000; // Límite de seguridad
        end

        // Periodo total de 20 ms para el servo = 540,000 ciclos de reloj
        if (counter < 20'd540000) 
            counter <= counter + 20'd1;
        else 
            counter <= 20'd0;

        // Generación del estado eléctrico del pin
        pwm_out <= (counter < duty_cycle);
    end
endmodule
