from .gate import Gate
from .gate_factory import GateFactory

class AndGate(Gate):
    def compute(self, val1, val2):
        return int(val1 and val2)

GateFactory.register_gate("AND", AndGate)