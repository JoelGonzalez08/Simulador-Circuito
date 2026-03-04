import customtkinter as ctk
from App.app_controller import AppController
from .controls_panel import ControlsPanel
from .circuit_canvas import CircuitCanvas

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MainWindow, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if MainWindow._is_initialized: 
            return
            
        super().__init__()
        MainWindow._is_initialized = True
        
        self.title("Simulador Lógico Pro - UTB 2026")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.state('zoomed')

        self.app_controller = AppController()

        # Canvas primero (pero lo empaquetamos a la derecha)
        self.canvas_area = CircuitCanvas(self)
        self.canvas_area.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Panel de control (Izquierda)
        self.controls_area = ControlsPanel(self, self.app_controller, self.canvas_area)
        self.controls_area.pack(side=ctk.LEFT, fill=ctk.Y, padx=(20, 0), pady=20)
        
        self.sidebar_visible = True
        self.toggle_btn = ctk.CTkButton(self, text="◀", width=30, command=self.toggle_sidebar,
                                       fg_color="#2b2b36", hover_color="#3a3a46")
        self.toggle_btn.place(x=340, y=20)
        
        # FORZAR ACTUALIZACIÓN INICIAL
        self.update_idletasks()
        self.controls_area.on_structure_change()
    
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.controls_area.pack_forget()
            self.toggle_btn.configure(text="▶")
            self.toggle_btn.place(x=20, y=20)
        else:
            # El truco es 'before=self.canvas_area' para que no se mueva al final
            self.controls_area.pack(side=ctk.LEFT, fill=ctk.Y, padx=(20, 0), pady=20, before=self.canvas_area)
            self.toggle_btn.configure(text="◀")
            self.toggle_btn.place(x=340, y=20)
        
        self.sidebar_visible = not self.sidebar_visible
        
        # Redibujar inmediatamente para ajustar las hitboxes y los niveles
        self.update_idletasks()
        if self.app_controller.circuit:
            self.canvas_area.draw_circuit(self.app_controller.circuit)