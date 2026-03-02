class InputNode:
    """Representa las entradas iniciales del circuito (hojas del árbol)"""
    def __init__(self, value=0, name=""):
        self.value = value
        self.name = name

    def set_value(self, value: int):
        self.value = value

    def evaluate(self) -> int:
        return self.value

class Circuit:
    """Contenedor principal del árbol de compuertas"""
    def __init__(self):
        self.root = None           # La compuerta final (Nivel 1, la salida)
        self.inputs =[]           # Lista de InputNodes (Entradas del usuario)
        self.levels = {}           # Diccionario {nivel: [lista_de_compuertas]}

    def evaluate(self) -> int:
        """Inicia la evaluación recursiva desde la raíz"""
        if self.root is None:
            raise ValueError("El circuito no tiene una compuerta raíz conectada.")
        return self.root.evaluate()