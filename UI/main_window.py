import tkinter as tk
from App.app_controller import AppController
from .controls_panel import ControlsPanel
from .circuit_canvas import CircuitCanvas

class MainWindow(tk.Tk):
    _instance = None  # Aquí guardamos la única instancia

    def __new__(cls):
        # Implementación del patrón Singleton
        if cls._instance is None:
            cls._instance = super(MainWindow, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Evitamos re-inicializar si el Singleton ya fue creado
        if '_initialized' in self.__dict__: 
            return
        super().__init__()
        self._initialized = True
        
        # Configuración básica de la ventana
        self.title("Simulador de Circuitos - Taller #1 Arquitectura del Computador")
        self.geometry("1100x650")
        self.configure(bg="#2c3e50")

        # 1. Instanciamos el Controlador (El "C" de MVC)
        self.app_controller = AppController()

        # 2. Creamos las Vistas: El Canvas (derecha) y el Panel (izquierda)
        self.canvas_area = CircuitCanvas(self)
        self.canvas_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Al panel le pasamos el controlador para que pueda darle órdenes, y el canvas para actualizarlo
        self.controls_area = ControlsPanel(self, self.app_controller, self.canvas_area)
        self.controls_area.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)