from .gate import Gate
from .gate_factory import GateFactory

class XorGate(Gate):
    def evaluate(self):
        val1 = self._get_val(self.input1)
        val2 = self._get_val(self.input2)
        return int(val1 ^ val2) # El operador ^ en Python es XOR
    
GateFactory.register_gate("XOR", XorGate)