from .gate import Gate
from .gate_factory import GateFactory

class OrGate(Gate):
    def compute(self, val1, val2):
        return int(val1 or val2)

GateFactory.register_gate("OR", OrGate)