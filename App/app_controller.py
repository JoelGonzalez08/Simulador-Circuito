# App/app_controller.py
from .tree_builder import CircuitBuilder

class AppController:
    def __init__(self):
        self.builder = CircuitBuilder()
        self.circuit = None
        self.input_states =[]

    def create_new_circuit(self, num_levels: int, gate_config: dict, ff_loc: str):
        num_inputs = 2 ** num_levels
        
        # Mantener los estados de las entradas si el tamaño no cambia
        if len(self.input_states) != num_inputs:
            self.input_states = [0] * num_inputs
            
        self.circuit = self.builder.build_circuit(num_levels, gate_config, ff_loc)
        self.set_inputs(self.input_states)
        return self.circuit

    def toggle_input(self, index: int):
        """Invertir el estado de una entrada al hacer click en el Canvas"""
        self.input_states[index] = 1 if self.input_states[index] == 0 else 0
        self.set_inputs(self.input_states)

    def set_inputs(self, values: list):
        if not self.circuit: return
        for node, val in zip(self.circuit.inputs, values):
            node.set_value(val)

    def run_simulation(self):
        if not self.circuit: return 0
        return self.circuit.evaluate()