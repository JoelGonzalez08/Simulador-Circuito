from .gate import Gate
from .gate_factory import GateFactory

class AndGate(Gate):
    def evaluate(self):
        val1 = self._get_val(self.input1)
        val2 = self._get_val(self.input2)
        return int(val1 and val2)

GateFactory.register_gate("AND", AndGate)