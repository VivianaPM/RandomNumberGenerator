import tkinter as tk
from tkinter import ttk
from AlgNoCong.cuadradoMedio import GeneradorApp as CuadradosMediosApp
from AlgCong.CongMulti import GeneradorCongruencialApp as CongruencialApp

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Generadores de Números Pseudoaleatorios")
        self.root.geometry("400x200")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Seleccione un Método", font=('Arial', 14)).pack(pady=10)
        
        # Botones para cada método
        ttk.Button(
            main_frame, 
            text="Cuadrados Medios", 
            command=self.open_cuadrados_medios
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Congruencial Lineal", 
            command=self.open_congruencial
        ).pack(fill=tk.X, pady=5)
        
        # Botón de salida
        ttk.Button(
            main_frame, 
            text="Salir", 
            command=self.root.quit
        ).pack(fill=tk.X, pady=10)
    
    def open_cuadrados_medios(self):
        new_window = tk.Toplevel(self.root)
        app = CuadradosMediosApp(new_window)
    
    def open_congruencial(self):
        new_window = tk.Toplevel(self.root)
        app = CongruencialApp(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()