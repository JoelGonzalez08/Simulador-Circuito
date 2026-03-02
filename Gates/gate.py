from abc import ABC, abstractmethod

class Gate(ABC):
    def __init__(self, input1=None, input2=None):
        self.input1 = input1
        self.input2 = input2

    def _get_val(self, node):
        """
        Si el nodo conectado es otra compuerta, llama a su evaluate().
        Si es un número directo (0 o 1), simplemente lo retorna.
        """
        if hasattr(node, 'evaluate'):
            return node.evaluate()
        return int(node) if node is not None else 0

    @abstractmethod
    def evaluate(self):
        pass