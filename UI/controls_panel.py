import tkinter as tk
from tkinter import ttk, messagebox

class ControlsPanel(tk.Frame):
    def __init__(self, parent, controller, canvas):
        super().__init__(parent, width=300, bg="#ecf0f1", relief=tk.RAISED, borderwidth=2)
        self.controller = controller
        self.canvas = canvas
        
        self.gate_vars = {} # Guardará las variables de los combobox por nivel
        self.input_vars =[] # Guardará las variables (0 o 1) de los botones de entrada
        
        self._build_ui()

    def _build_ui(self):
        # --- Título ---
        tk.Label(self, text="Configuración", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(pady=10)

        # --- N° de Niveles ---
        tk.Label(self, text="Cantidad de Niveles:", bg="#ecf0f1").pack()
        self.levels_var = tk.IntVar(value=2)
        tk.Spinbox(self, from_=1, to=4, textvariable=self.levels_var, command=self._generate_level_dropdowns).pack(pady=5)

        # --- Contenedor Dinámico para Tipos de Compuertas ---
        self.gates_frame = tk.Frame(self, bg="#ecf0f1")
        self.gates_frame.pack(fill=tk.X, padx=10, pady=5)
        self._generate_level_dropdowns() # Generar los iniciales

        # --- Bonus: Flip-Flop ---
        self.ff_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Bonus: Agregar Flip-Flop SR a la salida", variable=self.ff_var, bg="#ecf0f1").pack(pady=10)

        # --- Botón Construir ---
        tk.Button(self, text="1. Construir Circuito", bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                  command=self.build_circuit).pack(fill=tk.X, padx=10, pady=10)

        # --- Contenedor Dinámico para Entradas (0/1) ---
        tk.Label(self, text="Entradas del Circuito:", bg="#ecf0f1").pack()
        self.inputs_frame = tk.Frame(self, bg="#ecf0f1")
        self.inputs_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # --- Botón Evaluar ---
        tk.Button(self, text="2. Evaluar Circuito", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  command=self.evaluate_circuit).pack(fill=tk.X, padx=10, pady=10)

        # --- Requisito #6: Derechos de Autor ---
        creditos = "Autores: [Grupo 4]\nProfesor: Daniel Arias"
        tk.Label(self, text=creditos, bg="#ecf0f1", font=("Arial", 8, "italic"), fg="#7f8c8d").pack(side=tk.BOTTOM, pady=10)

    def _generate_level_dropdowns(self):
        """Genera dinámicamente los ComboBox para elegir la compuerta de cada nivel"""
        for widget in self.gates_frame.winfo_children():
            widget.destroy()
            
        self.gate_vars.clear()
        num_levels = self.levels_var.get()
        opciones =["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]

        for i in range(1, num_levels + 1):
            frame = tk.Frame(self.gates_frame, bg="#ecf0f1")
            frame.pack(fill=tk.X, pady=2)
            # El nivel 1 es la salida, el nivel N son las entradas. Lo mostramos amigable al usuario.
            tk.Label(frame, text=f"Nivel {i}:", width=8, anchor="w", bg="#ecf0f1").pack(side=tk.LEFT)
            
            var = tk.StringVar(value="AND")
            cb = ttk.Combobox(frame, textvariable=var, values=opciones, state="readonly", width=10)
            cb.pack(side=tk.RIGHT)
            self.gate_vars[i] = var

    def build_circuit(self):
        """Lee la UI, pide al Controlador que arme el circuito y redibuja."""
        num_levels = self.levels_var.get()
        gate_config = {level: var.get() for level, var in self.gate_vars.items()}
        use_ff = self.ff_var.get()

        # Le decimos al controlador que construya
        circuit = self.controller.create_new_circuit(num_levels, gate_config, use_ff)
        
        # Generamos los botones de las entradas
        self._generate_input_toggles(len(circuit.inputs))

        # Dibujamos en el Canvas (Obligamos a Tkinter a actualizar medidas primero)
        self.canvas.update_idletasks()
        self.canvas.draw_circuit(circuit)

    def _generate_input_toggles(self, num_inputs):
        """Crea botoncitos para alternar entre 0 y 1 en las entradas"""
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.input_vars.clear()

        # Usamos un grid para que no se vea feo si son 16 entradas (4 niveles)
        for i in range(num_inputs):
            var = tk.IntVar(value=0)
            self.input_vars.append(var)
            
            btn = tk.Checkbutton(self.inputs_frame, text=f"In_{i}", variable=var, bg="#ecf0f1", indicatoron=False, selectcolor="#2ecc71", width=5)
            btn.grid(row=i//4, column=i%4, padx=2, pady=2)

    def evaluate_circuit(self):
        """Envía las entradas al controlador, evalúa y actualiza la vista"""
        # 1. Recoger valores (0 o 1) de la UI
        input_values =[var.get() for var in self.input_vars]
        
        # 2. Enviar al controlador
        self.controller.set_inputs(input_values)
        resultado_final = self.controller.run_simulation()
        
        # 3. Obtener resultados parciales para los colores
        # (Esto lo mejoraremos en el canvas, por ahora re-dibujamos para reflejar cambios en las cajas de entrada)
        self.canvas.draw_circuit(self.controller.circuit)
        
        # 4. Mostrar Pop-up con el resultado
        messagebox.showinfo("Resultado", f"El resultado final del circuito es: {resultado_final}")