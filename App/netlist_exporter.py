"""
Exportador de circuitos a formato Netlist SPICE
Compatible con: Proteus, LTSpice, Multisim, ngspice
"""

class NetlistExporter:
    """Genera archivo netlist SPICE para compuertas lógicas"""
    
    # Mapeo de compuertas a modelos SPICE estándar
    GATE_MODELS = {
        "AND": "74LS08",
        "OR": "74LS32",
        "XOR": "74LS86",
        "NAND": "74LS00",
        "NOR": "74LS02",
        "XNOR": "74LS266",
        "NOT": "74LS04"
    }
    
    def __init__(self, circuit):
        self.circuit = circuit
        self.node_counter = 0
        self.node_map = {}  # Mapea objetos a nombres de nodos
        
    def _get_node_name(self, obj):
        """Obtiene o crea un nombre de nodo único para un objeto"""
        if id(obj) not in self.node_map:
            self.node_counter += 1
            self.node_map[id(obj)] = f"N{self.node_counter:03d}"
        return self.node_map[id(obj)]
    
    def export_spice(self, filename: str) -> str:
        """Exporta el circuito a formato SPICE netlist"""
        lines = []
        lines.append(f"* Circuit Netlist - Generado por Simulador Logico")
        lines.append(f"* Niveles: {len([k for k in self.circuit.levels.keys() if isinstance(k, int)])}")
        lines.append(f"* Entradas: {len(self.circuit.inputs)}")
        lines.append("")
        
        # Fuente de alimentación
        lines.append("* === ALIMENTACION ===")
        lines.append("VCC VCC 0 DC 5V")
        lines.append("GND 0 0 0")
        lines.append("")
        
        # Entradas (fuentes de voltaje)
        lines.append("* === ENTRADAS ===")
        for i, inp in enumerate(self.circuit.inputs):
            voltage = "5V" if inp.value == 1 else "0V"
            lines.append(f"V_IN{i} IN{i} 0 DC {voltage}")
            self.node_map[id(inp)] = f"IN{i}"
        lines.append("")
        
        # Compuertas por nivel
        lines.append("* === COMPUERTAS LOGICAS ===")
        gate_count = 0
        
        num_levels = max([k for k in self.circuit.levels.keys() if isinstance(k, int)])
        
        for level in range(num_levels, 0, -1):
            gates = self.circuit.levels[level]
            lines.append(f"* Nivel {level}")
            
            for i, gate in enumerate(gates):
                gate_count += 1
                gate_name = gate.__class__.__name__.replace("Gate", "").upper()
                model = self.GATE_MODELS.get(gate_name, "74LS00")
                
                # Obtener nodos de entrada
                in1_node = self.node_map.get(id(gate.input1), f"IN{2*i}")
                in2_node = self.node_map.get(id(gate.input2), f"IN{2*i+1}")
                
                # Nodo de salida
                if level == 1:
                    out_node = "OUT"
                else:
                    out_node = f"L{level}G{i}"
                
                self.node_map[id(gate)] = out_node
                
                # Formato SPICE subcircuit
                lines.append(f"X_U{gate_count} {in1_node} {in2_node} {out_node} VCC GND {model}")
        
        lines.append("")
        
        # Flip-Flop SR si existe
        if self.circuit.ff_node:
            lines.append("* === FLIP-FLOP SR ===")
            lines.append(f"* Ubicacion: {self.circuit.ff_target}")
            lines.append("X_FF1 S_IN R_IN Q_OUT Q_NOT VCC GND 74LS279")
            lines.append("")
        
        # Salida
        lines.append("* === SALIDA ===")
        lines.append(".PROBE V(OUT)")
        lines.append("")
        
        # Modelos de subcircuitos (definiciones básicas)
        lines.append("* === MODELOS DE COMPUERTAS ===")
        lines.append(".SUBCKT 74LS00 A B Y VCC GND")
        lines.append("* NAND Gate")
        lines.append(".ENDS")
        lines.append("")
        lines.append(".SUBCKT 74LS08 A B Y VCC GND")
        lines.append("* AND Gate")
        lines.append(".ENDS")
        lines.append("")
        lines.append(".SUBCKT 74LS32 A B Y VCC GND")
        lines.append("* OR Gate")
        lines.append(".ENDS")
        lines.append("")
        lines.append(".SUBCKT 74LS86 A B Y VCC GND")
        lines.append("* XOR Gate")
        lines.append(".ENDS")
        lines.append("")
        lines.append(".SUBCKT 74LS02 A B Y VCC GND")
        lines.append("* NOR Gate")
        lines.append(".ENDS")
        lines.append("")
        lines.append(".SUBCKT 74LS266 A B Y VCC GND")
        lines.append("* XNOR Gate")
        lines.append(".ENDS")
        lines.append("")
        
        lines.append(".END")
        
        content = "\n".join(lines)
        
        # Guardar archivo
        with open(filename, 'w') as f:
            f.write(content)
        
        return content
    
    def export_verilog(self, filename: str) -> str:
        """Exporta el circuito a formato Verilog"""
        lines = []
        num_inputs = len(self.circuit.inputs)
        num_levels = max([k for k in self.circuit.levels.keys() if isinstance(k, int)])
        
        lines.append(f"// Verilog - Generado por Simulador Logico")
        lines.append(f"module circuit_tree (")
        
        # Puertos
        input_ports = ", ".join([f"in{i}" for i in range(num_inputs)])
        lines.append(f"    input {input_ports},")
        lines.append(f"    output out")
        lines.append(f");")
        lines.append("")
        
        # Wires internos
        lines.append("// Wires internos")
        for level in range(num_levels, 1, -1):
            num_gates = 2 ** (level - 1)
            for i in range(num_gates):
                lines.append(f"wire w_L{level}G{i};")
        lines.append("")
        
        # Instancias de compuertas
        lines.append("// Compuertas")
        for level in range(num_levels, 0, -1):
            gates = self.circuit.levels[level]
            
            for i, gate in enumerate(gates):
                gate_name = gate.__class__.__name__.replace("Gate", "").lower()
                
                # Determinar entradas
                if level == num_levels:
                    in1 = f"in{2*i}"
                    in2 = f"in{2*i+1}"
                else:
                    in1 = f"w_L{level+1}G{2*i}"
                    in2 = f"w_L{level+1}G{2*i+1}"
                
                # Determinar salida
                out = "out" if level == 1 else f"w_L{level}G{i}"
                
                # Verilog gate primitive
                if gate_name in ["and", "or", "xor", "nand", "nor", "xnor"]:
                    lines.append(f"{gate_name} g_L{level}G{i} ({out}, {in1}, {in2});")
        
        lines.append("")
        lines.append("endmodule")
        
        content = "\n".join(lines)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        return content
