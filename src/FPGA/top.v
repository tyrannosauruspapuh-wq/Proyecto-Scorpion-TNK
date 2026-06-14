// Versión 1.2.3 del módulo top para la Tang Nano 9K
// Control de 2 Servos y 2 motores, datos enviados por UART desde el ESP32 en formato de 8 bits, corrección del código en el apartado de UART
// Mejora de filtrado de ruido eléctrico.
// Corrección de los comandos L y R 
// Corrección de los Servomotores, mejora de procesamiento de la señal.
// Autor Jesús Osvaldo Yáñez Mancilla, fecha: 27/05/2026
module tank_controller (
    input clk,            // 27MHz nativos de la Tang Nano 9K
    input rx,             // Línea proveniente del TX del ESP32
    output reg [3:0] motors = 4'b0000, 
    output pwm_j,         
    output pwm_k          
);

parameter CLK_FREQ = 27000000;
parameter BAUD_RATE = 9600;
parameter [16:0] WAIT_TIME = CLK_FREQ / BAUD_RATE; 

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

reg [7:0] angulo_j = 8'd90; 
reg [7:0] angulo_k = 8'd90;

// --- RECEPTOR UART ULTRA-ROBUSTO CON MUESTREO EN EL CENTRO ---
reg [3:0] state = 4'd0; // 0: Idle, 1: Start, 2..9: Data bits, 10: Stop
reg [16:0] clk_count = 17'd0;

always @(posedge clk) begin
    case (state)
        4'd0: begin // IDLE: Esperando flanco de bajada (bit de START)
            clk_count <= 17'd0;
            if (rx_sync == 1'b0) begin
                state <= 4'd1;
            end
        end
        
        4'd1: begin // Bit de START: Esperamos hasta la mitad del bit para validar
            if (clk_count < (WAIT_TIME / 2) - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                if (rx_sync == 1'b0) begin // Validado
                    state <= 4'd2; // Pasar al primer bit de datos
                end else begin
                    state <= 4'd0; // Falsa alarma (ruido)
                end
            end
        end
        
        4'd2, 4'd3, 4'd4, 4'd5, 4'd6, 4'd7, 4'd8, 4'd9: begin // Bits de datos (0 al 7)
            if (clk_count < WAIT_TIME - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                data_raw[state - 4'd2] <= rx_sync; // Muestreo en el centro exacto del bit
                state <= state + 4'd1;
            end
        end
        
        4'd10: begin // Bit de STOP
            if (clk_count < WAIT_TIME - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                state <= 4'd0; // Regresar a IDLE
                
                // --- PROCESAMIENTO DE COMANDOS ---
                if (state_mode == 2'd1) begin
                    if (data_raw <= 8'd180) angulo_j <= data_raw;
                    state_mode <= 2'd0;
                end else if (state_mode == 2'd2) begin
                    if (data_raw <= 8'd180) angulo_k <= data_raw;
                    state_mode <= 2'd0;
                end else begin
                    case (data_raw)
                        8'h01: motors <= 4'b1010; // Adelante (F)
                        8'h02: motors <= 4'b0101; // Atrás (B)
                        8'h03: motors <= 4'b0110; // Izquierda (L)
                        8'h04: motors <= 4'b1001; // Derecha (R)
                        8'h00: motors <= 4'b0000; // Parar (S)
                        8'hAA: state_mode <= 2'd1; // Cabecera Servo J
                        8'hBB: state_mode <= 2'd2; // Cabecera Servo K
                        default: motors <= motors;
                    endcase
                end
            end
        end
        default: state <= 4'd0;
    endcase
end

servo_pwm control_j (.clk(clk), .angle(angulo_j), .pwm_out(pwm_j));
servo_pwm control_k (.clk(clk), .angle(angulo_k), .pwm_out(pwm_k));

endmodule

// MÓDULO PWM OPTIMIZADO
module servo_pwm (
    input clk,
    input [7:0] angle,
    output reg pwm_out
);
    reg [19:0] counter = 20'd0;
    wire [19:0] duty_cycle;

    // Usar lógica combinacional (wire) para que el duty cycle cambie instantáneamente 
    // sin esperar un ciclo de reloj extra que arruine la comparación.
    assign duty_cycle = 20'd27000 + ((angle > 8'd180 ? 8'd180 : angle) * 20'd150);

    always @(posedge clk) begin
        if (counter < 20'd540000 - 1) 
            counter <= counter + 20'd1;
        else 
            counter <= 20'd0;

        pwm_out <= (counter < duty_cycle);
    end
endmodule
