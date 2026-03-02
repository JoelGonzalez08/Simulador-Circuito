from .gate import Gate
from .gate_factory import GateFactory

class NandGate(Gate):
    def evaluate(self):
        val1 = self._get_val(self.input1)
        val2 = self._get_val(self.input2)
        return int(not (val1 and val2))
    
GateFactory.register_gate("NAND", NandGate)