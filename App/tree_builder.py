# App/tree_builder.py
from Gates.gate_factory import GateFactory
from .circuit import Circuit, InputNode

class CircuitBuilder:
    def __init__(self):
        self.circuit = Circuit()

    def build_circuit(self, num_levels: int, gate_types_per_level: dict):
        """
        gate_types_per_level: dict {1: "AND", 2: "OR", 3: "XOR"...}
        El nivel 1 es la salida final (raíz). El nivel 'num_levels' es el más cercano a las entradas.
        """
        self.circuit = Circuit() # Reiniciamos el circuito
        
        # 1. Crear las entradas (Hojas). Para N niveles, hay 2^N entradas.
        num_inputs = 2 ** num_levels
        current_nodes =[InputNode(value=0, name=f"In_{i}") for i in range(num_inputs)]
        self.circuit.inputs = current_nodes
        
        # 2. Construir por niveles (desde el nivel más profundo hasta el nivel 1)
        for level in range(num_levels, 0, -1):
            # Obtenemos qué compuerta pidió el usuario para este nivel (Por defecto AND si falta)
            gate_type = gate_types_per_level.get(level, "AND")
            
            # N° de compuertas por nivel = 2^(nivel - 1)
            num_gates = 2 ** (level - 1)
            level_gates =[]
            
            # Agrupamos los nodos actuales de 2 en 2 para conectarlos a las nuevas compuertas
            for i in range(num_gates):
                left_node = current_nodes[2 * i]
                right_node = current_nodes[2 * i + 1]
                
                # Usamos nuestra Factory para instanciar la compuerta y conectarle sus 2 hijos
                gate = GateFactory.create(gate_type, left_node, right_node)
                level_gates.append(gate)
                
            # Guardamos las compuertas de este nivel para poder consultar resultados parciales después
            self.circuit.levels[level] = level_gates
            
            # Las compuertas recién creadas serán las "entradas" del siguiente nivel superior
            current_nodes = level_gates
            
        # 3. Al terminar el bucle, solo quedará 1 compuerta en current_nodes (El nivel 1 tiene 2^0 = 1)
        self.circuit.root = current_nodes[0]
        
        return self.circuit
    
    def attach_flip_flop(self):
        """Envuelve la salida final (raíz) con un Flip-Flop SR"""
        if not self.circuit.root:
            return
        
        # Conectamos la salida del circuito al pin 'S' (Set) y un 0 fijo al 'R' (Reset).
        sr_ff = GateFactory.create("SR", self.circuit.root, 0)
        self.circuit.root = sr_ff
        
        # Lo agregamos al diccionario de niveles como un "Nivel 0" (Bonus)
        self.circuit.levels[0] = [sr_ff]