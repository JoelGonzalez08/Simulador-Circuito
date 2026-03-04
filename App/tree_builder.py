# App/tree_builder.py
from Gates.gate_factory import GateFactory
from .circuit import Circuit, InputNode

class QNotProxy:
    """Simula la salida Q' del Flip-Flop para inyectarla en la compuerta siguiente"""
    def __init__(self, ff_node):
        self.ff_node = ff_node
    def evaluate(self):
        return 1 if self.ff_node.state == 0 else 0

class CircuitBuilder:
    def __init__(self):
        self.circuit = Circuit()

    def build_circuit(self, num_levels: int, gate_types_per_level: dict, ff_location: str = "Ninguno"):
        self.circuit = Circuit()
        num_inputs = 2 ** num_levels
        current_nodes =[InputNode(0, f"In_{i}") for i in range(num_inputs)]
        self.circuit.inputs = current_nodes
        
        # 1. Construir el árbol estándar
        for level in range(num_levels, 0, -1):
            gate_type = gate_types_per_level.get(level, "AND")
            num_gates = 2 ** (level - 1)
            level_gates =[]
            for i in range(num_gates):
                gate = GateFactory.create(gate_type, current_nodes[2*i], current_nodes[2*i+1])
                level_gates.append(gate)
            self.circuit.levels[level] = level_gates
            current_nodes = level_gates
            
        self.circuit.root = current_nodes[0]
        self.circuit.ff_node = None
        self.circuit.ff_target = None # Guardará (Nivel, Indice) o "Salida Final"
        
        # 2. INYECTAR EL FLIP-FLOP DINÁMICAMENTE EN CUALQUIER COMPUERTA
        if ff_location == "Salida Final":
            ff = GateFactory.create("SR", self.circuit.root, 0)
            self.circuit.root = ff
            self.circuit.ff_node = ff
            self.circuit.ff_target = "Salida Final"
            
        elif ff_location.startswith("Nivel"):
            # Formato: "Nivel 3 - Comp 0"
            parts = ff_location.split()
            lvl = int(parts[1])
            comp_i = int(parts[4])
            
            target_gate = self.circuit.levels[lvl][comp_i]
            
            # El FF roba las entradas que iban hacia la compuerta objetivo
            gate_S = target_gate.input1
            gate_R = target_gate.input2
            
            ff = GateFactory.create("SR", gate_S, gate_R)
            self.circuit.ff_node = ff
            self.circuit.ff_target = (lvl, comp_i)
            
            # La compuerta objetivo ahora recibe Q y Q' del Flip-Flop
            target_gate.input1 = ff
            target_gate.input2 = QNotProxy(ff)
            
        return self.circuit