// Versión 2.0.1 del módulo top para la Tang Nano 9K
// Control de 2 Servos y 2 motores, datos enviados por UART desde el ESP32 en formato de 8 bits
// Se elimina la línea 190 previamente presente en la versión anterior debido a preoblemas de sintesis.
// Autor Jesús Osvaldo Yáñez Mancilla, fecha: 28/05/2026
module tank_controller (
    input clk,                // 27MHz nativos de la Tang Nano 9K
    input rx,                 // Línea proveniente del TX del ESP32
    
    // --- PINES PARA EL SENSOR ULTRASÓNICO ---
    input sensor_echo,        // Pin Echo (¡Recuerda el divisor de tensión a 3.3V!)
    output sensor_trigger,    // Pin Trigger (Pulso de disparo de 10us)
    
    // --- PINES DE CONTROL PARA EL DRIVER TB6612FNG ---
    output reg AIN1 = 1'b0,   // Dirección Motor A (Izquierdo)
    output reg AIN2 = 1'b0,
    output reg BIN1 = 1'b0,   // Dirección Motor B (Derecho)
    output reg BIN2 = 1'b0,
    output PWMA,              // Habilitación / Velocidad Motor A
    output PWMB,              // Habilitación / Velocidad Motor B
    
    // --- PINES DE CONTROL PARA LOS SERVOS ---
    output pwm_j,         
    output pwm_k          
);

// Mantenemos la velocidad de los motores al 100%. STBY del driver a 3.3V.
assign PWMA = 1'b1;
assign PWMB = 1'b1;

parameter CLK_FREQ = 27000000;
parameter BAUD_RATE = 9600;
parameter [16:0] WAIT_TIME = CLK_FREQ / BAUD_RATE; // 2812 ciclos por bit

// --- TRIPLE ETAPA DE SINCRONIZACIÓN CONTRA METAESTABILIDAD ---
reg rx_stage1, rx_stage2, rx_sync;
always @(posedge clk) begin
    rx_stage1 <= rx;
    rx_stage2 <= rx_stage1;
    rx_sync   <= rx_stage2;
end

// Registros internos de la UART
reg [16:0] clk_count = 17'd0;
reg [3:0] state = 4'd0;       
reg [7:0] data_raw = 8'd0;
reg [1:0] state_mode = 2'd0; 

// Registros de ángulos para los servos
reg [7:0] angulo_j = 8'd90; 
reg [7:0] angulo_k = 8'd90;

// --- INSTANCIACIÓN DEL RADAR ULTRASÓNICO ---
wire objeto_al_frente;

ultrasonic_detector radar (
    .clk(clk),
    .echo(sensor_echo),
    .trigger(sensor_trigger),
    .obstaculo(objeto_al_frente)
);


// --- RECEPTOR UART CON MUESTREO EN EL CENTRO ---
always @(posedge clk) begin
    case (state)
        4'd0: begin // IDLE
            clk_count <= 17'd0;
            if (rx_sync == 1'b0) state <= 4'd1;
        end
        
        4'd1: begin // START
            if (clk_count < (WAIT_TIME / 2) - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                if (rx_sync == 1'b0) state <= 4'd2; 
                else                 state <= 4'd0; 
            end
        end
        
        4'd2, 4'd3, 4'd4, 4'd5, 4'd6, 4'd7, 4'd8, 4'd9: begin // DATA
            if (clk_count < WAIT_TIME - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                data_raw[state - 4'd2] <= rx_sync; 
                state <= state + 4'd1;
            end
        end
        
        4'd10: begin // STOP
            if (clk_count < WAIT_TIME - 1) begin
                clk_count <= clk_count + 17'd1;
            end else begin
                clk_count <= 17'd0;
                state <= 4'd0; 
                
                // --- PROCESAMIENTO DE COMANDOS ---
                if (state_mode == 2'd1) begin
                    if (data_raw <= 8'd180) angulo_j <= data_raw;
                    state_mode <= 2'd0;
                end else if (state_mode == 2'd2) begin
                    if (data_raw <= 8'd180) angulo_k <= data_raw;
                    state_mode <= 2'd0;
                end else begin
                    case (data_raw)
                        // Adelante (F): Solo se permite si el camino está despejado
                        8'h01: begin 
                            if (!objeto_al_frente) begin
                                AIN1 <= 1'b1; AIN2 <= 1'b0; 
                                BIN1 <= 1'b1; BIN2 <= 1'b0; 
                            end else begin
                                AIN1 <= 1'b0; AIN2 <= 1'b0; 
                                BIN1 <= 1'b0; BIN2 <= 1'b0;
                            end
                        end
                        // Atrás (B)
                        8'h02: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b1; 
                            BIN1 <= 1'b0; BIN2 <= 1'b1; 
                        end
                        // Izquierda (L)
                        8'h03: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b1; 
                            BIN1 <= 1'b1; BIN2 <= 1'b0; 
                        end
                        // Derecha (R)
                        8'h04: begin 
                            AIN1 <= 1'b1; AIN2 <= 1'b0; 
                            BIN1 <= 1'b0; BIN2 <= 1'b1; 
                        end
                        // Parar (S)
                        8'h00: begin 
                            AIN1 <= 1'b0; AIN2 <= 1'b0; 
                            BIN1 <= 1'b0; BIN2 <= 1'b0; 
                        end
                        
                        8'hAA: state_mode <= 2'd1; 
                        8'hBB: state_mode <= 2'd2; 
                        default: begin
                            // Mapeo dinámico de protección: si vamos hacia adelante y detecta algo, frena
                            if (objeto_al_frente && AIN1 == 1'b1 && BIN1 == 1'b1) begin
                                AIN1 <= 1'b0; AIN2 <= 1'b0;
                                BIN1 <= 1'b0; BIN2 <= 1'b0;
                            end else begin
                                AIN1 <= AIN1; AIN2 <= AIN2;
                                BIN1 <= BIN1; BIN2 <= BIN2;
                            end
                        end
                    endcase
                end
            end
        end
        default: state <= 4'd0;
    endcase
end

// --- ESCUDO INTERRUPTOR ASÍNCRONO DE EMERGENCIA ---
// Si el tanque está avanzando y el sensor cambia a 1 en CUALQUIER momento (fuera de la UART),
// este bloque quita la tracción delantera instantáneamente en el próximo ciclo de reloj.
always @(posedge clk) begin
    if (objeto_al_frente && AIN1 == 1'b1 && BIN1 == 1'b1) begin
        AIN1 <= 1'b0; AIN2 <= 1'b0;
        BIN1 <= 1'b0; BIN2 <= 1'b0;
    end
end

// --- INSTANCIACIÓN DE MÓDULOS PWM ---
servo_pwm control_j (.clk(clk), .angle(angulo_j), .pwm_out(pwm_j));
servo_pwm control_k (.clk(clk), .angle(angulo_k), .pwm_out(pwm_k));

endmodule


// =========================================================================
// --- SUBMÓDULO: DETECTOR ULTRASÓNICO (HC-SR04) ---
// =========================================================================
module ultrasonic_detector (
    input clk,               
    input echo,              
    output reg trigger = 0,  
    output reg obstaculo = 0 
);
    reg [21:0] clk_trigger = 22'd0;
    reg [21:0] echo_count = 22'd0;
    reg echo_past = 1'b0;

    // 1. GENERADOR DE TRIGGER: Envía un pulso de 10us cada 60ms
    // 60ms @ 27MHz = 1,620,000 ciclos. 10us = 270 ciclos.
    always @(posedge clk) begin
        if (clk_trigger < 22'd1620000) begin
            clk_trigger <= clk_trigger + 22'd1;
            trigger <= (clk_trigger < 22'd270); 
        end else begin
            clk_trigger <= 22'd0;
        end
    end

    // 2. MEDIDOR DE ANCHO DE PULSO (Mapeo de distancia)
    // Umbral de 15 cm * 1566 ciclos por cm = 23,490 ciclos de reloj
    always @(posedge clk) begin
        echo_past <= echo;
        
        if (echo) begin
            if (echo_count < 22'd200000) begin // Evitar desbordamiento por rebote infinito
                echo_count <= echo_count + 22'd1;
            end
        end else if (echo_past && !echo) begin
            // Flanco de bajada detectado: Terminó de leer el pulso de eco
            if (echo_count < 22'd23490 && echo_count > 22'd300) begin
                obstaculo <= 1'b1; // ¡Obstáculo detectado a menos de 15cm!
            end else begin
                obstaculo <= 1'b0; // Camino libre
            end
            echo_count <= 22'd0;
        end
    end
endmodule


// =========================================================================
// --- SUBMÓDULO: SERVO PWM ---
// =========================================================================
module servo_pwm (
    input clk,
    input [7:0] angle,
    output reg pwm_out
);
    reg [19:0] counter = 20'd0;
    wire [19:0] duty_cycle;

    assign duty_cycle = 20'd27000 + ((angle > 8'd180 ? 8'd180 : angle) * 20'd150); 

    always @(posedge clk) begin
        if (counter < 20'd540000 - 1) 
            counter <= counter + 20'd1;
        else 
            counter <= 20'd0;

        pwm_out <= (counter < duty_cycle);
    end
endmodule
