from .gate import Gate
from .gate_factory import GateFactory
class NotGate(Gate):
    def evaluate(self):
        val1 = self._get_val(self.input1)
        # Ignoramos input2 porque NOT solo invierte 1 señal
        return int(not val1)
    
GateFactory.register_gate("NOT", NotGate)