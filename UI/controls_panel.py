import customtkinter as ctk
from tkinter import filedialog, messagebox
from App.netlist_exporter import NetlistExporter

class ControlsPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, controller, canvas):
        super().__init__(parent, width=300, corner_radius=15)
        self.controller = controller
        self.canvas = canvas
        self.canvas.on_input_toggle = self.handle_canvas_click
        self.gate_vars = {}
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill=ctk.X, padx=10, pady=(10, 5))
        ctk.CTkLabel(header, text="⚡ Panel de Control", font=ctk.CTkFont(size=18, weight="bold"), text_color="#00ffcc").pack(side=ctk.LEFT)
        
        self.theme_var = ctk.StringVar(value="dark")
        ctk.CTkSwitch(header, text="🌞/🌙", variable=self.theme_var, onvalue="light", offvalue="dark", command=self.toggle_theme, width=40).pack(side=ctk.RIGHT)

        frame_niv = ctk.CTkFrame(self, fg_color="transparent")
        frame_niv.pack(fill=ctk.X, padx=10, pady=10)
        ctk.CTkLabel(frame_niv, text="Niveles:", font=ctk.CTkFont(size=14)).pack(side=ctk.LEFT)
        
        self.levels_var = ctk.StringVar(value="3") 
        ctk.CTkComboBox(frame_niv, values=["1", "2", "3", "4", "5", "6"], variable=self.levels_var, command=self.on_structure_change, width=80).pack(side=ctk.RIGHT)

        self.gates_frame = ctk.CTkScrollableFrame(self, height=150, corner_radius=10)
        self.gates_frame.pack(fill=ctk.X, padx=10, pady=10)

        ctk.CTkLabel(self, text="Ubicación Flip-Flop SR:", font=ctk.CTkFont(size=13, weight="bold")).pack(padx=10, anchor="w")
        self.ff_var = ctk.StringVar(value="Ninguno")
        self.ff_combo = ctk.CTkComboBox(self, variable=self.ff_var, command=self.build_and_evaluate)
        self.ff_combo.pack(fill=ctk.X, padx=10, pady=5)

        self.btn_reset_ff = ctk.CTkButton(self, text="Resetear Memoria FF", fg_color="#e74c3c", command=self.reset_flipflop)
        self.btn_reset_ff.pack(fill=ctk.X, padx=10, pady=5)

        # Separador
        ctk.CTkLabel(self, text="─" * 30, text_color="#555").pack(pady=8)
        
        # Botones de exportación
        ctk.CTkLabel(self, text="Exportar Circuito:", font=ctk.CTkFont(size=13, weight="bold")).pack(padx=10, anchor="w")
        
        export_frame = ctk.CTkFrame(self, fg_color="transparent")
        export_frame.pack(fill=ctk.X, padx=10, pady=5)
        
        self.btn_export_spice = ctk.CTkButton(export_frame, text="📄 SPICE (.cir)", fg_color="#3498db", 
                                               command=self.export_spice, width=120)
        self.btn_export_spice.pack(side=ctk.LEFT, padx=(0, 5))
        
        self.btn_export_verilog = ctk.CTkButton(export_frame, text="📄 Verilog (.v)", fg_color="#9b59b6", 
                                                 command=self.export_verilog, width=120)
        self.btn_export_verilog.pack(side=ctk.RIGHT)
        
        # Separador
        ctk.CTkLabel(self, text="─" * 30, text_color="#555").pack(pady=8)
        
        # Información del equipo
        ctk.CTkLabel(self, text="Integrantes:", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=10, anchor="w")
        
        integrantes = [
            "• Álvaro Jesús Ayala Alcalá",
            "• Bianca Mastrascusa Camargo",
            "• Joel David González Barros",
            "• Maykol Stiven Madrid Romero",
            "• Sofía Mejía González"
        ]
        for nombre in integrantes:
            ctk.CTkLabel(self, text=nombre, font=ctk.CTkFont(size=10), text_color="#aaaaaa").pack(padx=15, anchor="w")
        
        ctk.CTkLabel(self, text="").pack(pady=2)  # Espaciador
        ctk.CTkLabel(self, text="Docente:", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=10, anchor="w")
        ctk.CTkLabel(self, text="Daniel Andrés Arias López", font=ctk.CTkFont(size=10), text_color="#aaaaaa").pack(padx=15, anchor="w", pady=(0, 10))

    def export_spice(self):
        if not self.controller.circuit:
            messagebox.showwarning("Aviso", "No hay circuito para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".cir",
            filetypes=[("SPICE Netlist", "*.cir"), ("Netlist", "*.net"), ("Todos", "*.*")],
            title="Exportar Netlist SPICE"
        )
        if filename:
            exporter = NetlistExporter(self.controller.circuit)
            exporter.export_spice(filename)
            messagebox.showinfo("Éxito", f"Circuito exportado a:\n{filename}\n\nCompatible con Proteus, LTSpice, Multisim")

    def export_verilog(self):
        if not self.controller.circuit:
            messagebox.showwarning("Aviso", "No hay circuito para exportar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".v",
            filetypes=[("Verilog", "*.v"), ("Todos", "*.*")],
            title="Exportar Verilog"
        )
        if filename:
            exporter = NetlistExporter(self.controller.circuit)
            exporter.export_verilog(filename)
            messagebox.showinfo("Éxito", f"Circuito exportado a:\n{filename}\n\nCompatible con ModelSim, Quartus, Vivado")

    def on_structure_change(self, *args):
        for widget in self.gates_frame.winfo_children(): widget.destroy()
        self.gate_vars.clear()
        num_niveles = int(self.levels_var.get())
        opciones =["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]

        for i in range(1, num_niveles + 1):
            f = ctk.CTkFrame(self.gates_frame, fg_color="transparent")
            f.pack(fill=ctk.X, pady=5)
            ctk.CTkLabel(f, text=f"Nivel {i}:").pack(side=ctk.LEFT)
            var = ctk.StringVar(value="AND")
            cb = ctk.CTkComboBox(f, variable=var, values=opciones, width=120, command=self.build_and_evaluate)
            cb.pack(side=ctk.RIGHT)
            self.gate_vars[i] = var
            
        ff_options =["Ninguno"]
        for lvl in range(num_niveles, 0, -1):
            for i in range(2 ** (lvl - 1)):
                ff_options.append(f"Nivel {lvl} - Comp {i}")
        
        self.ff_combo.configure(values=ff_options)
        self.build_and_evaluate()

    def build_and_evaluate(self, *args):
        gate_config = {l: v.get() for l, v in self.gate_vars.items()}
        self.controller.create_new_circuit(int(self.levels_var.get()), gate_config, self.ff_var.get())
        self.controller.run_simulation()
        self.canvas.draw_circuit(self.controller.circuit)

    def handle_canvas_click(self, index):
        self.controller.toggle_input(index)
        self.controller.run_simulation()
        self.canvas.draw_circuit(self.controller.circuit)

    def toggle_theme(self):
        self.canvas.set_theme(self.theme_var.get())

    def reset_flipflop(self):
        if self.controller.circuit and self.controller.circuit.ff_node:
            self.controller.circuit.ff_node.state = 0
            self.controller.run_simulation()
            self.canvas.draw_circuit(self.controller.circuit)