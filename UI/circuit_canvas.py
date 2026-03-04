import tkinter as tk
import math

class CircuitCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)
        self.current_circuit = None
        self.on_input_toggle = None
        self.input_hitboxes = []
        
        # Pan & Zoom state
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.zoom_level = 1.0
        self._pan_start_x = 0
        self._pan_start_y = 0
        self._is_panning = False
        self._initialized = False
        
        # Bindings
        self.bind("<Button-1>", self.on_click)
        
        # Pan: botón central (rueda) o botón derecho
        self.bind("<ButtonPress-2>", self._start_pan)
        self.bind("<B2-Motion>", self._do_pan)
        self.bind("<ButtonRelease-2>", self._end_pan)
        self.bind("<ButtonPress-3>", self._start_pan)
        self.bind("<B3-Motion>", self._do_pan)
        self.bind("<ButtonRelease-3>", self._end_pan)
        
        # Zoom con rueda del ratón
        self.bind("<MouseWheel>", self._on_mousewheel)
        
        # Reset con doble click central
        self.bind("<Double-Button-2>", self._reset_view)
        self.bind("<Double-Button-3>", self._reset_view)
        
        # Esperar a que el canvas tenga dimensiones antes de dibujar
        self.bind("<Configure>", self._on_configure)
        
        self.set_theme("dark")
    
    def _on_configure(self, event):
        """Redibujar cuando el canvas cambia de tamaño."""
        if event.width > 1 and event.height > 1:
            self._initialized = True
            if self.current_circuit:
                self.after_idle(lambda: self.draw_circuit(self.current_circuit))
    
    def _start_pan(self, event):
        """Iniciar pan."""
        self._is_panning = True
        self._pan_start_x = event.x
        self._pan_start_y = event.y
        self.config(cursor="fleur")
    
    def _do_pan(self, event):
        """Mover la vista."""
        if not self._is_panning:
            return
        dx = event.x - self._pan_start_x
        dy = event.y - self._pan_start_y
        self.pan_offset_x += dx
        self.pan_offset_y += dy
        self._pan_start_x = event.x
        self._pan_start_y = event.y
        if self.current_circuit:
            self.draw_circuit(self.current_circuit)
    
    def _end_pan(self, event):
        """Terminar pan."""
        self._is_panning = False
        self.config(cursor="")
    
    def _on_mousewheel(self, event):
        """Zoom con rueda del ratón."""
        # Calcular nuevo nivel de zoom
        if event.delta > 0:
            new_zoom = min(self.zoom_level * 1.1, 3.0)
        else:
            new_zoom = max(self.zoom_level / 1.1, 0.3)
        
        # Ajustar offset para hacer zoom centrado en el cursor
        if self.zoom_level != new_zoom:
            scale_factor = new_zoom / self.zoom_level
            self.pan_offset_x = event.x - (event.x - self.pan_offset_x) * scale_factor
            self.pan_offset_y = event.y - (event.y - self.pan_offset_y) * scale_factor
            self.zoom_level = new_zoom
            
            if self.current_circuit:
                self.draw_circuit(self.current_circuit)
    
    def _reset_view(self, event=None):
        """Resetear pan y zoom."""
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.zoom_level = 1.0
        if self.current_circuit:
            self.draw_circuit(self.current_circuit)

    def _transform(self, x, y):
        """Transforma coordenadas lógicas a coordenadas de pantalla."""
        return (x * self.zoom_level + self.pan_offset_x, 
                y * self.zoom_level + self.pan_offset_y)
    
    def _inverse_transform(self, sx, sy):
        """Transforma coordenadas de pantalla a coordenadas lógicas."""
        return ((sx - self.pan_offset_x) / self.zoom_level,
                (sy - self.pan_offset_y) / self.zoom_level)

    def set_theme(self, mode):
        if mode == "dark":
            self.bg_color, self.grid_color = "#12121a", "#1c1c28"
            self.text_color, self.gate_bg = "#1e1e2e", "#1e1e2e"
            self.gate_border = "#5c5c77"
            self.color_1, self.color_0 = "#00ffcc", "#ff3366"
            self.label_color = "#ffffff"  # Color para etiquetas (niveles, letras, LED)
            self.gate_text_color = "#ffffff"  # Texto dentro de compuertas
            self.input_text_on, self.input_text_off = "#000000", "#ffffff"
        else:
            self.bg_color, self.grid_color = "#e8e8ec", "#d8d8dc"
            self.text_color, self.gate_bg = "#f5f5f5", "#1a2530"
            self.gate_border = "#2c3e50"
            self.color_1, self.color_0 = "#008866", "#cc2020"  # Colores más saturados
            self.label_color = "#1a1a2e"  # Color oscuro para etiquetas
            self.gate_text_color = "#ffffff"  # Texto dentro de compuertas (fondo oscuro)
            self.input_text_on, self.input_text_off = "#000000", "#ffffff"
        self.configure(bg=self.bg_color)
        if self.current_circuit: self.draw_circuit(self.current_circuit)

    def on_click(self, event):
        # Transformar coordenadas del click a coordenadas lógicas
        lx, ly = self._inverse_transform(event.x, event.y)
        for (x1, y1, x2, y2, i) in self.input_hitboxes:
            if x1 <= lx <= x2 and y1 <= ly <= y2:
                if self.on_input_toggle: self.on_input_toggle(i)
                break

    def _draw_vector_gate(self, x, y, gate_type, active=False, tag="circuit_elements"):
        w, h = 54, 44
        outline_color = self.color_1 if active else self.gate_border
        in_x, out_x = x - w//2, x + w//2
        in1_y, in2_y = y - h//3, y + h//3
        
        if gate_type in["AND", "NAND"]:
            self.create_rectangle(in_x, y-h//2, x, y+h//2, fill=self.gate_bg, outline="", width=0, tags=tag)
            self.create_arc(in_x, y-h//2, out_x, y+h//2, start=-90, extent=180, fill=self.gate_bg, outline="", width=0, style=tk.CHORD, tags=tag)
            self.create_arc(in_x, y-h//2, out_x, y+h//2, start=-90, extent=180, outline=outline_color, width=2, style=tk.ARC, tags=tag)
            self.create_line(in_x, y-h//2, x, y-h//2, fill=outline_color, width=2, tags=tag)
            self.create_line(in_x, y+h//2, x, y+h//2, fill=outline_color, width=2, tags=tag)
            self.create_line(in_x, y-h//2, in_x, y+h//2, fill=outline_color, width=2, tags=tag)
            if gate_type == "NAND":
                self.create_oval(out_x, y-5, out_x+10, y+5, fill=self.gate_bg, outline=outline_color, width=2, tags=tag)
                out_x += 10
                
        elif gate_type in ["OR", "NOR", "XOR", "XNOR"]:
            pts =[]
            back_curve =[(in_x + 10 * math.cos(-math.pi/2 + (i/15)*math.pi), y + (h//2) * math.sin(-math.pi/2 + (i/15)*math.pi)) for i in range(16)]
            offset = 12 if "X" in gate_type else 0
            if "X" in gate_type:
                self.create_line([(px - 6, py) for px, py in back_curve], fill=outline_color, width=2, smooth=True, tags=tag)
                in_x -= 6

            pts.append(back_curve[-1])
            for i in range(16):
                t = i / 15
                pts.append((back_curve[-1][0] + offset + t * (out_x - back_curve[-1][0] - offset), y + h//2 - (h//2) * math.pow(t, 1.5)))
            for i in range(15, -1, -1):
                t = i / 15
                pts.append((back_curve[0][0] + offset + t * (out_x - back_curve[0][0] - offset), y - h//2 + (h//2) * math.pow(t, 1.5)))
            pts.extend(back_curve)
            
            self.create_polygon(pts, fill=self.gate_bg, outline=outline_color, width=2, smooth=True, tags=tag)
            if "N" in gate_type:
                self.create_oval(out_x, y-5, out_x+10, y+5, fill=self.gate_bg, outline=outline_color, width=2, tags=tag)
                out_x += 10
                
        self.create_text(x + (5 if gate_type in["OR", "NOR", "XOR", "XNOR"] else 0), y, text=gate_type, fill=self.gate_text_color, font=("Segoe UI", 8, "bold"), tags=tag)
        return in_x, in1_y, in2_y, out_x, y

    def draw_circuit(self, circuit):
        self.delete("all")
        self.input_hitboxes.clear()
        self.current_circuit = circuit
        if not circuit: return

        # Esperar a que el canvas tenga dimensiones válidas
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1 or height <= 1:
            # Programar redibujado para cuando tenga dimensiones
            self.after(50, lambda: self.draw_circuit(circuit))
            return

        # Dibujar fondo sólido primero para evitar flickering
        self.create_rectangle(0, 0, width, height, fill=self.bg_color, outline="")

        # Aplicar transformaciones de zoom/pan
        z = self.zoom_level
        ox, oy = self.pan_offset_x, self.pan_offset_y

        # Cuadrícula (extendida para pan)
        grid_size = int(40 * z)
        if grid_size > 5:  # Solo dibujar si es visible
            start_x = int(ox % grid_size) - grid_size
            start_y = int(oy % grid_size) - grid_size
            for i in range(start_x, width + grid_size, max(grid_size, 1)):
                self.create_line(i, 0, i, height, fill=self.grid_color, width=1)
            for i in range(start_y, height + grid_size, max(grid_size, 1)):
                self.create_line(0, i, width, i, fill=self.grid_color, width=1)

        num_levels = len([k for k in circuit.levels.keys() if isinstance(k, int) and k != 0])
        num_inputs = len(circuit.inputs)
        
        # Dimensiones base del circuito - escalan según complejidad
        # Mínimo 150px de ancho por nivel, mínimo 50px de alto por entrada
        min_width_per_level = 150
        min_height_per_input = 50
        
        base_width = max(width, num_levels * min_width_per_level + 200)
        base_height = max(height, num_inputs * min_height_per_input + 100)
        x_spacing = base_width / (num_levels + 1.5)
        
        # Tag para elementos del circuito (para aplicar transformación)
        circuit_tag = "circuit_elements"
        
        # DIBUJO DE NIVELES
        box_colors =["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#e67e22"] 
        for level in range(num_levels, 0, -1):
            col_index = num_levels - level + 1 
            x_center = x_spacing * (col_index + 0.5)
            c_idx = (level - 1) % len(box_colors)
            self.create_rectangle(x_center - 40, 20, x_center + 40, base_height - 20, outline=box_colors[c_idx], width=4, tags=circuit_tag)
            self.create_text(x_center, 10, text=f"Nivel {level}", fill=self.label_color, font=("Georgia", 14, "italic"), tags=circuit_tag)

        node_positions = {} 
        y_spacing_inputs = base_height / (num_inputs + 1)
        
        # 1. ENTRADAS
        for i, input_node in enumerate(circuit.inputs):
            x, y = x_spacing * 0.5, y_spacing_inputs * (i + 1)
            node_positions[f"in_{i}"] = (x + 15, y, input_node.value)
            
            color = self.color_1 if input_node.value == 1 else self.gate_bg
            text_col = self.input_text_on if input_node.value == 1 else self.input_text_off
            
            pts =[x-15, y-10, x+5, y-10, x+15, y, x+5, y+10, x-15, y+10]
            self.create_polygon(pts, fill=color, outline=self.gate_border, width=2, tags=circuit_tag)
            self.create_text(x-2, y, text=str(input_node.value), fill=text_col, font=("Consolas", 12, "bold"), tags=circuit_tag)
            
            # Círculos de conexión
            self.create_oval(x+16, y-3, x+20, y+3, fill=self.gate_border, outline="", tags=circuit_tag)
            self.create_oval(x+22, y-3, x+26, y+3, fill=self.gate_border, outline="", tags=circuit_tag)
            
            if i % 2 == 0:
                y_next = y_spacing_inputs * (i + 2) if i+1 < num_inputs else y
                letter = chr(65 + (i//2)) 
                self.create_text(x-35, (y + y_next)/2, text=letter, fill=self.label_color, font=("Segoe UI", 16, "bold"), tags=circuit_tag)
            
            # Guardar hitbox en coordenadas lógicas (sin transformar)
            self.input_hitboxes.append((x-15, y-10, x+15, y+10, i))

        # 2. COMPUERTAS Y FLIP-FLOP (Manteniendo tu lógica SR-FF)
        for level in range(num_levels, 0, -1):
            gates = circuit.levels[level]
            y_spacing = base_height / (len(gates) + 1)
            col_index = num_levels - level + 1 
            x = x_spacing * (col_index + 0.5)

            for i, gate in enumerate(gates):
                y = y_spacing * (i + 1)
                gate_val = getattr(gate, 'last_result', 0)
                gate_name = gate.__class__.__name__.replace("Gate", "").upper()
                
                in_x, in1_y, in2_y, out_x, out_y = self._draw_vector_gate(x, y, gate_name, active=(gate_val==1), tag=circuit_tag)
                node_positions[id(gate)] = (out_x, out_y, gate_val)

                if level == num_levels:
                    c1, c2 = node_positions[f"in_{2*i}"], node_positions[f"in_{2*i+1}"]
                else:
                    prev = circuit.levels[level + 1]
                    c1, c2 = node_positions[id(prev[2*i])], node_positions[id(prev[2*i+1])]

                # LÓGICA DE INYECCIÓN SR-FF ORIGINAL
                if circuit.ff_target == (level, i):
                    ff = circuit.ff_node
                    x_ff = (c1[0] + in_x) / 2
                    
                    self.create_rectangle(x_ff-25, in1_y-15, x_ff+25, in2_y+15, fill=self.gate_bg, outline="#f39c12", width=2, tags=circuit_tag)
                    self.create_text(x_ff, y, text="SR-FF", fill=self.gate_text_color, font=("Segoe UI", 9, "bold"), tags=circuit_tag)
                    self.create_text(x_ff-15, in1_y, text="S", fill=self.gate_text_color, font=("Segoe UI", 8), tags=circuit_tag)
                    self.create_text(x_ff-15, in2_y, text="R", fill=self.gate_text_color, font=("Segoe UI", 8), tags=circuit_tag)
                    self.create_text(x_ff+15, in1_y, text="Q", fill=self.gate_text_color, font=("Segoe UI", 8), tags=circuit_tag)
                    self.create_text(x_ff+15, in2_y, text="Q'", fill=self.gate_text_color, font=("Segoe UI", 8), tags=circuit_tag)

                    for origin, target_y in[(c1, in1_y), (c2, in2_y)]:
                        w_col = self.color_1 if origin[2] == 1 else self.color_0
                        lw = 3 if origin[2] == 1 else 1.5
                        self.create_line(origin[0], origin[1], x_ff-35, origin[1], fill=w_col, width=lw, tags=circuit_tag)
                        self.create_line(x_ff-35, origin[1], x_ff-35, target_y, fill=w_col, width=lw, tags=circuit_tag)
                        self.create_line(x_ff-35, target_y, x_ff-25, target_y, fill=w_col, width=lw, tags=circuit_tag)

                    col_Q = self.color_1 if ff.state == 1 else self.color_0
                    col_Q_not = self.color_1 if ff.state == 0 else self.color_0
                    self.create_line(x_ff+25, in1_y, in_x, in1_y, fill=col_Q, width=3 if ff.state==1 else 1.5, tags=circuit_tag)
                    self.create_line(x_ff+25, in2_y, in_x, in2_y, fill=col_Q_not, width=3 if ff.state==0 else 1.5, tags=circuit_tag)
                else:
                    x_mid = (c1[0] + in_x) / 2
                    for origin, target_y in[(c1, in1_y), (c2, in2_y)]:
                        w_col = self.color_1 if origin[2] == 1 else self.color_0
                        lw = 3 if origin[2] == 1 else 1.5
                        self.create_line(origin[0], origin[1], x_mid, origin[1], fill=w_col, width=lw, tags=circuit_tag)
                        self.create_line(x_mid, origin[1], x_mid, target_y, fill=w_col, width=lw, tags=circuit_tag)
                        self.create_line(x_mid, target_y, in_x, target_y, fill=w_col, width=lw, tags=circuit_tag)

        # 3. SALIDA FINAL - LED DIODO
        final_out = node_positions[id(circuit.levels[1][0])]
        lx, ly = final_out[0], final_out[1]
        out_val = final_out[2]
        
        col_led = self.color_1 if out_val == 1 else self.color_0
        self.create_line(lx, ly, lx + 20, ly, fill=col_led, width=3 if out_val==1 else 1.5, tags=circuit_tag)
        self.create_polygon(lx+20, ly-10, lx+20, ly+10, lx+35, ly, fill=self.gate_bg, outline=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+35, ly-10, lx+35, ly+10, fill=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+35, ly, lx+45, ly, fill=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+45, ly, lx+45, ly+15, fill=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+35, ly+15, lx+55, ly+15, fill=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+40, ly+20, lx+50, ly+20, fill=col_led, width=2, tags=circuit_tag)
        self.create_line(lx+43, ly+25, lx+47, ly+25, fill=col_led, width=2, tags=circuit_tag)
        self.create_text(lx+28, ly-22, text="D1\nLED", fill=self.label_color, font=("Segoe UI", 8, "bold"), tags=circuit_tag)
        
        # Aplicar transformación de pan/zoom a elementos del circuito
        if self.zoom_level != 1.0:
            self.scale(circuit_tag, 0, 0, self.zoom_level, self.zoom_level)
        if self.pan_offset_x != 0 or self.pan_offset_y != 0:
            self.move(circuit_tag, self.pan_offset_x, self.pan_offset_y)