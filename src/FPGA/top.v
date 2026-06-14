// Versión 1.3.0 del módulo top para la Tang Nano 9K
// Control de 2 Servos y 2 motores, datos enviados por UART desde el ESP32 en formato de 8 bits, corrección del código en el apartado de UART
// Se cambia al driver TB6612FNG, se actualiza el código top.v
// Autor Jesús Osvaldo Yáñez Mancilla, fecha: 27/05/2026
module tank_controller (
    input clk,            // 27MHz nativos de la Tang Nano 9K
    input rx,             // Línea proveniente del TX del ESP32
    
    // --- PINES DE CONTROL PARA EL DRIVER TB6612FNG ---
    output reg AIN1 = 1'b0, // Dirección Motor A (Izquierdo)
    output reg AIN2 = 1'b0,
    output reg BIN1 = 1'b0, // Dirección Motor B (Derecho)
    output reg BIN2 = 1'b0,
    output PWMA,            // Habilitación / Velocidad Motor A
    output PWMB,            // Habilitación / Velocidad Motor B
    
    // --- PINES DE CONTROL PARA LOS SERVOS ---
    output pwm_j,         
    output pwm_k          
);

// Mantenemos la velocidad de los motores al 100% de manera fija.
// RECUERDA: Conectar el pin STBY del TB6612FNG directo a 3.3V en tu hardware.
assign PWMA = 1'b1;
assign PWMB = 1'b1;

parameter CLK_FREQ = 27000000;
parameter BAUD_RATE = 9600;
parameter [16:0] WAIT_TIME = CLK_FREQ / BAUD_RATE; // 2812 ciclos exactos por bit

// --- TRIPLE ETAPA DE SINCRONIZACIÓN CONTRA METAESTABILIDAD ---
reg rx_stage1, rx_stage2, rx_sync;
always @(posedge clk) begin
    rx_stage1 <= rx;
    rx_stage2 <= rx_stage1;
    rx_sync   <= rx_stage2;
end

// Registros internos del receptor y estados
reg [16:0] clk_count = 17'd0;
reg [3:0] state = 4'd0;       // Máquina de estados UART (0 a 10)
reg [7:0] data_raw = 8'd0;
reg [1:0] state_mode = 2'd0; 

// Registros estables de salida hacia los módulos PWM de los servos
reg [7:0] angulo_j = 8'd90; 
reg [7:0] angulo_k = 8'd90;

// --- RECEPTOR UART ULTRA-ROBUSTO CON MUESTREO EN EL CENTRO ---
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
                if (rx_sync == 1'b0) begin // Validado con éxito
                    state <= 4'd2; 
                end else begin
                    state <= 4'd0; // Falsa alarma por ruido eléctrico
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
                state <= 4'd0; // Regresar a IDLE de forma síncrona
                
                // --- PROCESAMIENTO DE COMANDOS UNIFICADO ---
                if (state_mode == 2'd1) begin
                    if (data_raw <= 8'd180) angulo_j <= data_raw;
                    state_mode <= 2'd0;
                end else if (state_mode == 2'd2) begin
                    if (data_raw <= 8'd180) angulo_k <= data_raw;
                    state_mode <= 2'd0;
                end else begin
                    case (data_raw)
                        // Adelante (F): Ambos motores avanzan
                        8'h01: begin 
                            AIN1 <= 1'b1; AIN2 <= 1'b0; 
                            BIN1 <= 1'b1; BIN2 <= 1'b0; 
                        end
                        // Atrás (B): Ambos motores retroceden
                        8'h02: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b1; 
                            BIN1 <= 1'b0; BIN2 <= 1'b1; 
                        end
                        // Izquierda (L): Motor A atrás, Motor B adelante (Giro sobre su propio eje)
                        8'h03: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b1; 
                            BIN1 <= 1'b1; BIN2 <= 1'b0; 
                        end
                        // Derecha (R): Motor A adelante, Motor B atrás
                        8'h04: begin 
                            AIN1 <= 1'b1; AIN2 <= 1'b0; 
                            BIN1 <= 1'b0; BIN2 <= 1'b1; 
                        end
                        // Parar (S): Freno corto (ambos terminales a GND)
                        8'h00: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b0; 
                            BIN1 <= 1'b0; BIN2 <= 1'b0; 
                        end
                        
                        8'hAA: state_mode <= 2'd1; // Cabecera Servo J
                        8'hBB: state_mode <= 2'd2; // Cabecera Servo K
                        default: begin // Mantener el estado actual de los motores ante datos basura
                            AIN1 <= AIN1; AIN2 <= AIN2;
                            BIN1 <= BIN1; BIN2 <= BIN2;
                        end
                    endcase
                end
            end
        end
        default: state <= 4'd0;
    endcase
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


// --- MÓDULO AUXILIAR PWM CALIBRADO A 27MHz (OPTIMIZADO) ---
module servo_pwm (
    input clk,
    input [7:0] angle,
    output reg pwm_out
);
    reg [19:0] counter = 20'd0;
    wire [19:0] duty_cycle;

    // Se calcula dinámicamente con lógica combinacional para evitar desfases de reloj
    assign duty_cycle = 20'd27000 + ((angle > 8'd180 ? 8'd180 : angle) * 20'd150); 

    always @(posedge clk) begin
        // Periodo total de 20 ms para el servo = 540,000 ciclos de reloj - 1
        if (counter < 20'd540000 - 1) 
            counter <= counter + 20'd1;
        else 
            counter <= 20'd0;

        // Salida limpia basada en el comparador síncrono
        pwm_out <= (counter < duty_cycle);
    end
endmodule
