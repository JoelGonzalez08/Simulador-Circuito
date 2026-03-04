from .gate import Gate
from .gate_factory import GateFactory

class NorGate(Gate):
    def compute(self, val1, val2):
        return int(not (val1 or val2))
    
GateFactory.register_gate("NOR", NorGate)