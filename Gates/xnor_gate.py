from .gate import Gate
from .gate_factory import GateFactory

class XnorGate(Gate):
    def compute(self, val1, val2):
        return int(not (val1 ^ val2))
    
GateFactory.register_gate("XNOR", XnorGate)