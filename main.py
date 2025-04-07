import tkinter as tk 
from interface import MainMenu

if __name__ == '__main__':
   
    root = tk.Tk()
    root.title("Generador de numeros pseudoaleatorios")
    app = MainMenu(root)
    root.mainloop()