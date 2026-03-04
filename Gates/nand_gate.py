from .gate import Gate
from .gate_factory import GateFactory

class NandGate(Gate):
    def compute(self, val1, val2):
        return int(not (val1 and val2))
    
GateFactory.register_gate("NAND", NandGate)