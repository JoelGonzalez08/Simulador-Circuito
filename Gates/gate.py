# Gates/gate.py
from abc import ABC, abstractmethod

class Gate(ABC):
    def __init__(self, input1=None, input2=None):
        self.input1 = input1
        self.input2 = input2
        self.last_result = 0  # <--- NUEVO: Memoria del último cálculo para la UI

    def _get_val(self, node):
        if hasattr(node, 'evaluate'):
            return node.evaluate()
        return int(node) if node is not None else 0

    @abstractmethod
    def compute(self, val1, val2):
        """Método matemático interno"""
        pass

    def evaluate(self):
        # <--- NUEVO: Separamos la evaluación recursiva de la matemática
        val1 = self._get_val(self.input1)
        val2 = self._get_val(self.input2)
        self.last_result = self.compute(val1, val2)
        return self.last_result