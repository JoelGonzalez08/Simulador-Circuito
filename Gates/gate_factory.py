class GateFactory:
    _registry = {}
    @classmethod
    def register_gate(cls, name: str, gate_class):
        cls._registry[name.upper()] = gate_class

    @classmethod
    def create(cls, name: str, a, b):
        gate_class = cls._registry.get(name.upper())
        if not gate_class:
            raise ValueError(f"Compuerta '{name}' no está registrada en la Factory.")
        return gate_class(a, b)