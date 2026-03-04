from .gate import Gate
from .gate_factory import GateFactory

class XorGate(Gate):
    def compute(self, val1, val2):
        return int(val1 ^ val2)
    
GateFactory.register_gate("XOR", XorGate)