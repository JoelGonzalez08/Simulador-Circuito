from .gate import Gate
from .gate_factory import GateFactory

class SRFlipFlop(Gate):
    def __init__(self, input1=None, input2=None):
        # input1 será S (Set) e input2 será R (Reset)
        super().__init__(input1, input2)
        self.state = 0  # El Flip-Flop tiene memoria, inicia en 0 (Q = 0)

    def compute(self, val1, val2):
        # Obtenemos los valores de Set (S) y Reset (R)
        s = val1
        r = val2
        
        # Lógica del Flip-Flop SR:
        if s == 1 and r == 0:
            self.state = 1      # Set: Enciende
        elif s == 0 and r == 1:
            self.state = 0      # Reset: Apaga
        elif s == 0 and r == 0:
            pass                # Memoria: Mantiene el estado anterior (no hace nada)
        elif s == 1 and r == 1:
            # Estado inválido en un SR normal. 
            # Dependiendo del diseño, a veces se asume 0, o se mantiene el estado.
            # Lo dejaremos en 0 por convención de seguridad.
            self.state = 0      

        return self.state

GateFactory.register_gate("SR", SRFlipFlop)