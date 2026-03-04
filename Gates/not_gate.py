from .gate import Gate
from .gate_factory import GateFactory
class NotGate(Gate):
    def compute(self, val1):
        return int(not val1)
    
GateFactory.register_gate("NOT", NotGate)