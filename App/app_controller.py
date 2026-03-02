from .tree_builder import CircuitBuilder

class AppController:
    def __init__(self):
        self.builder = CircuitBuilder()
        self.circuit = None

    def create_new_circuit(self, num_levels: int, gate_config: dict, use_flip_flop: bool = False):
        """Ordena la construcción de un nuevo circuito."""
        self.circuit = self.builder.build_circuit(num_levels, gate_config)
        
        if use_flip_flop:
            self.builder.attach_flip_flop()
            
        return self.circuit

    def set_inputs(self, input_values: list):
        """Recibe una lista de 0s y 1s de la UI y los inyecta en el árbol."""
        if not self.circuit:
            raise Exception("Debes crear un circuito primero.")
            
        if len(input_values) != len(self.circuit.inputs):
            raise ValueError(f"Se esperaban {len(self.circuit.inputs)} entradas, pero se recibieron {len(input_values)}.")
            
        for node, value in zip(self.circuit.inputs, input_values):
            node.set_value(value)

    def run_simulation(self) -> int:
        """Ejecuta el circuito y devuelve el resultado final."""
        if not self.circuit:
            return 0
        return self.circuit.evaluate()

    def get_partial_results(self, level: int) -> list:
        """
        Requisito de la UI: 'Luces verdes para 1 y luces rojas para 0 en resultados parciales'.
        Este método devuelve una lista con los valores de las compuertas en un nivel específico.
        """
        if not self.circuit or level not in self.circuit.levels:
            return[]
            
        # Evaluamos cada compuerta de ese nivel para saber su estado actual
        return[gate.evaluate() for gate in self.circuit.levels[level]]