import tkinter as tk
from tkinter import ttk, messagebox
import random

class GeneradorCongruencialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Congruencial Lineal")
        
        # Variables con valores pequeños por defecto (0-10)
        self.a_var = tk.StringVar(value=str(random.randint(1, 10)))
        self.c_var = tk.StringVar(value=str(random.randint(0, 10)))
        self.m_var = tk.StringVar(value=str(random.randint(1, 10)))
        self.x0_var = tk.StringVar()
        self.current_x = None
        self.generando = False
        self.valores_generados = set()
        
        # Inicializar interfaz primero
        self.crear_interfaz()
        
        # Luego generar X0 inicial
        self.generar_x0()
    
    def generar_parametros(self):
        """Genera nuevos parámetros pequeños (0-10)"""
        self.a_var.set(str(random.randint(1, 10)))
        self.c_var.set(str(random.randint(0, 10)))
        self.m_var.set(str(random.randint(2, 10)))  # m debe ser al menos 2
        self.generar_x0()
    
    def generar_x0(self):
        """Genera un valor aleatorio para X0 entre 1 y m-1"""
        m = int(self.m_var.get()) if self.m_var.get().isdigit() else 10
        semilla = random.randint(1, max(1, m-1))
        self.x0_var.set(str(semilla))
        self.current_x = semilla
        self.valores_generados = {self.current_x}
        self.valor_actual_label.config(text=f"Valor actual de X₀: {self.current_x}")
        self.estado_label.config(text="Listo para generar", fg="black")
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def generar_numeros(self):
        """Genera números pseudoaleatorios hasta completar el ciclo"""
        if self.generando:
            return
            
        try:
            a = int(self.a_var.get())
            c = int(self.c_var.get())
            m = int(self.m_var.get())
            
            if m <= 1:
                messagebox.showerror("Error", "El módulo (m) debe ser mayor que 1")
                return
            
            # Limpiar el treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Configurar estado
            self.generando = True
            self.boton_generar.config(state="disabled")
            self.boton_semilla.config(state="disabled")
            self.boton_parametros.config(state="disabled")
            self.estado_label.config(text="Generando...", fg="blue")
            self.root.update()
            
            # Generar los números
            x = self.current_x
            paso = 1
            ciclo_completo = False
            self.valores_generados = {x}  # Reiniciar con la semilla actual
            
            while True:
                nuevo_x = (a * x + c) % m
                normalizado = nuevo_x / m if m != 0 else 0
                
                # Verificar si el valor ya fue generado (ciclo completo)
                if nuevo_x in self.valores_generados:
                    # Insertar la línea de repetición
                    self.tree.insert("", "end", values=(f"*{paso}", x, a, c, m, nuevo_x, f"{normalizado:.6f}"), tags=('repetido',))
                    ciclo_completo = True
                    self.estado_label.config(text=f"Ciclo completo detectado (Longitud: {paso-1})", fg="green")
                    break
                
                # Insertar en el treeview
                self.tree.insert("", "end", values=(paso, x, a, c, m, nuevo_x, f"{normalizado:.6f}"))
                
                # Actualizar para la siguiente iteración
                self.valores_generados.add(nuevo_x)
                x = nuevo_x
                paso += 1
                
                # Actualizar la interfaz periódicamente
                if paso % 5 == 0:
                    self.valor_actual_label.config(text=f"Valor actual de X₀: {x}")
                    self.root.update()
            
            # Actualizar el valor actual
            self.current_x = x
            self.valor_actual_label.config(text=f"Valor actual de X₀: {self.current_x}")
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores enteros válidos")
        finally:
            self.generando = False
            self.boton_generar.config(state="normal")
            self.boton_semilla.config(state="normal")
            self.boton_parametros.config(state="normal")
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz gráfica"""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()
        
        # Título
        tk.Label(main_frame, text="Generador Congruencial Lineal", 
                font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Panel de parámetros
        param_frame = tk.LabelFrame(main_frame, text="Parámetros (0-10)", padx=10, pady=10)
        param_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Entradas
        tk.Label(param_frame, text="Multiplicador (a):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(param_frame, textvariable=self.a_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(param_frame, text="Incremento (c):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(param_frame, textvariable=self.c_var, width=5).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(param_frame, text="Módulo (m):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(param_frame, textvariable=self.m_var, width=5).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(param_frame, text="Semilla inicial (X₀):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(param_frame, textvariable=self.x0_var, state='readonly', width=5).grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.boton_parametros = tk.Button(btn_frame, text="Nuevos Parámetros", command=self.generar_parametros)
        self.boton_parametros.pack(side="left", padx=5)
        
        self.boton_semilla = tk.Button(btn_frame, text="Nueva Semilla", command=self.generar_x0)
        self.boton_semilla.pack(side="left", padx=5)
        
        self.boton_generar = tk.Button(btn_frame, text="Generar Ciclo", command=self.generar_numeros, bg="#4CAF50", fg="white")
        self.boton_generar.pack(side="left", padx=5)
        
        # Etiquetas de estado
        self.valor_actual_label = tk.Label(main_frame, text="Valor actual de X₀: -", 
                                         font=("Arial", 10, "bold"))
        self.valor_actual_label.grid(row=3, column=0, columnspan=3, pady=5)
        
        self.estado_label = tk.Label(main_frame, text="Listo para generar", font=("Arial", 10))
        self.estado_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Treeview para mostrar resultados
        self.tree = ttk.Treeview(main_frame, columns=("Paso", "Xₙ", "a", "c", "m", "Xₙ₊₁", "Normalizado"), 
                               show="headings", height=8)
        
        # Configurar columnas
        columnas = [
            ("Paso", 50),
            ("Xₙ", 50),
            ("a", 40),
            ("c", 40),
            ("m", 40),
            ("Xₙ₊₁", 50),
            ("Normalizado", 80)
        ]
        
        for col, width in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # Configurar estilo para la fila repetida
        self.tree.tag_configure('repetido', background='#ffdddd', font=('Arial', 9, 'bold'))
        
        self.tree.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Fórmula
        tk.Label(main_frame, text="Fórmula: Xₙ₊₁ = (a × Xₙ + c) mod m", 
               font=("Arial", 10)).grid(row=6, column=0, columnspan=3, pady=10)