import tkinter as tk

class CircuitCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="#ecf0f1", highlightthickness=2, highlightbackground="#bdc3c7")

    def draw_circuit(self, circuit, partial_results=None):
        """Dibuja el árbol del circuito. partial_results es un dict {nivel:[resultados]}"""
        self.delete("all")  # Limpiamos el lienzo
        if not circuit:
            return

        width = self.winfo_width()
        height = self.winfo_height()
        
        # Si el canvas no se ha renderizado aún, damos tamaños por defecto
        if width <= 1: width = 800
        if height <= 1: height = 600

        # Calcular cuántas columnas necesitamos (Entradas + Niveles)
        num_levels = len([k for k in circuit.levels.keys() if k != 0])
        total_columns = num_levels + 2 # +1 para entradas, +1 para margen derecho
        x_spacing = width / total_columns

        node_positions = {} # Guardará las coordenadas (x,y) de cada nodo para dibujar las líneas

        # 1. DIBUJAR ENTRADAS (Columna 0, la más a la izquierda)
        num_inputs = len(circuit.inputs)
        y_spacing_inputs = height / (num_inputs + 1)
        
        for i, input_node in enumerate(circuit.inputs):
            x = x_spacing * 0.5
            y = y_spacing_inputs * (i + 1)
            node_positions[f"in_{i}"] = (x, y)
            
            # Color verde si es 1, rojo si es 0
            color = "#2ecc71" if input_node.value == 1 else "#e74c3c"
            self.create_rectangle(x-15, y-15, x+15, y+15, fill=color, outline="black")
            self.create_text(x, y, text=str(input_node.value), fill="white", font=("Arial", 10, "bold"))

        # 2. DIBUJAR COMPUERTAS POR NIVELES (De izquierda a derecha)
        # Los niveles en tu lógica van de N (más cercano a entradas) a 1 (raíz)
        for level in range(num_levels, 0, -1):
            gates = circuit.levels[level]
            num_gates = len(gates)
            y_spacing = height / (num_gates + 1)
            
            # Columna visual (1 es la pegada a las entradas, num_levels es la salida)
            col_index = num_levels - level + 1 
            x = x_spacing * (col_index + 0.5)

            for i, gate in enumerate(gates):
                y = y_spacing * (i + 1)
                # Guardamos la posición usando el ID de memoria del objeto compuerta
                node_positions[id(gate)] = (x, y)
                
                # Dibujar compuerta (Caja azul)
                name = gate.__class__.__name__.replace("Gate", "")
                self.create_rectangle(x-25, y-15, x+25, y+15, fill="#3498db", outline="black")
                self.create_text(x, y, text=name, fill="white", font=("Arial", 9, "bold"))

                # DIBUJAR LÍNEAS hacia sus hijos (izquierda)
                # Como es un árbol binario perfecto, la compuerta i está conectada a los hijos 2*i y 2*i+1 del nivel anterior
                if level == num_levels:
                    # Se conecta a las entradas
                    child1_pos = node_positions[f"in_{2*i}"]
                    child2_pos = node_positions[f"in_{2*i+1}"]
                else:
                    # Se conecta al nivel anterior (level + 1)
                    prev_gates = circuit.levels[level + 1]
                    child1_pos = node_positions[id(prev_gates[2*i])]
                    child2_pos = node_positions[id(prev_gates[2*i+1])]

                # Determinar color de la línea (verde=1, rojo=0) basado en resultados parciales
                line_color1, line_color2 = "black", "black"
                if partial_results:
                    # Lógica para colorear las líneas según el valor que viaja por ellas
                    pass # (Aquí iría la lógica fina de extraer los colores del dict partial_results, por ahora las dibujamos negras para tener la base)

                self.create_line(child1_pos[0]+15, child1_pos[1], x-25, y-5, fill=line_color1, width=2)
                self.create_line(child2_pos[0]+15, child2_pos[1], x-25, y+5, fill=line_color2, width=2)

        # 3. BONUS FLIP-FLOP (Si existe, nivel 0)
        if 0 in circuit.levels:
            ff = circuit.levels[0][0]
            x = x_spacing * (num_levels + 1.5)
            y = height / 2
            
            self.create_rectangle(x-30, y-20, x+30, y+20, fill="#f39c12")
            self.create_text(x, y, text=f"SR-FF\nQ={ff.state}", fill="white")
            
            # Conectar la raíz al FlipFlop
            root_gate = circuit.levels[1][0]
            root_pos = node_positions[id(root_gate)]
            self.create_line(root_pos[0]+25, root_pos[1], x-30, y, fill="black", width=2)