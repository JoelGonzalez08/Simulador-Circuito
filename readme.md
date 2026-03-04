# Simulador de Circuitos Lógicos

Simulador visual de circuitos digitales con compuertas lógicas organizadas en estructura de árbol binario. Permite diseñar, visualizar y exportar circuitos a formatos estándar de la industria.

## Características

- **Estructura de árbol binario**: Circuitos de 1 a 6 niveles (2 a 64 entradas)
- **Compuertas disponibles**: AND, OR, XOR, NAND, NOR, XNOR
- **Flip-Flop SR**: Insertable en cualquier posición del circuito
- **Visualización interactiva**: 
  - Click en entradas para cambiar valores
  - Pan (arrastrar con botón derecho)
  - Zoom (rueda del ratón)
- **Temas**: Modo claro y oscuro
- **Exportación**: Netlist SPICE (.cir) y Verilog (.v)

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

### Controles

| Acción | Control |
|--------|---------|
| Cambiar entrada | Click izquierdo en entrada |
| Mover vista | Arrastrar con botón derecho |
| Zoom | Rueda del ratón |
| Resetear vista | Doble click derecho |

### Exportación

El simulador permite exportar circuitos a:

- **SPICE Netlist (.cir)**: Compatible con Proteus, LTSpice, Multisim
- **Verilog (.v)**: Compatible con ModelSim, Quartus, Vivado

## Estructura del Proyecto

```
simulador_circuito/
├── main.py              # Punto de entrada
├── App/
│   ├── app_controller.py    # Controlador principal
│   ├── circuit.py           # Modelo del circuito
│   ├── tree_builder.py      # Constructor del árbol
│   └── netlist_exporter.py  # Exportador SPICE/Verilog
├── Gates/
│   ├── gate.py              # Clase base de compuertas
│   ├── gate_factory.py      # Fábrica de compuertas
│   ├── and_gate.py          # Compuerta AND
│   ├── or_gate.py           # Compuerta OR
│   ├── xor_gate.py          # Compuerta XOR
│   ├── nand_gate.py         # Compuerta NAND
│   ├── nor_gate.py          # Compuerta NOR
│   ├── xnor_gate.py         # Compuerta XNOR
│   ├── not_gate.py          # Compuerta NOT
│   └── sr_flipflop.py       # Flip-Flop SR
└── UI/
    ├── main_window.py       # Ventana principal
    ├── controls_panel.py    # Panel de controles
    └── circuit_canvas.py    # Canvas de visualización
```

## Arquitectura

El simulador utiliza el patrón **árbol binario** donde:

- Cada nivel tiene `2^(nivel-1)` compuertas
- Nivel N conecta a `2^N` entradas
- La salida final está en el Nivel 1

```
Nivel 3:  [G] [G] [G] [G]   ← 4 compuertas, 8 entradas
              ↘ ↙   ↘ ↙
Nivel 2:      [G]   [G]     ← 2 compuertas
                 ↘ ↙
Nivel 1:         [G]        ← 1 compuerta (salida)
                  ↓
                 LED
```

## Licencia

Proyecto académico - UTB 2026