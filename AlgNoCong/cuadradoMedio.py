import sys
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def generar_cuadrados_medios(semilla, corridas):
    resultados = []
    for i in range(corridas):
        semilla_al_cuadrado = semilla * semilla
        s = str(semilla_al_cuadrado).zfill(8)  # Rellenar con ceros hasta 8 dígitos
        t = s[2:6]  # Tomar los 4 dígitos centrales
        v = int(t)
        r = v / 10000
        resultados.append({
            'iteracion': i,
            'semilla': semilla,
            'cuadrado': semilla_al_cuadrado,
            'pseudoaleatorio': v,
            'random_ri': r
        })
        semilla = v
        if v == 0:
            break
    return resultados

def exportar_a_csv(resultados, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            campos = ['iteracion', 'semilla', 'cuadrado', 'pseudoaleatorio', 'random_ri']
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False

# Interfaz gráfica modificada
class GeneradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Pseudoaleatorios")
        
        # Variables para controlar la tabla
        self.tree = None
        self.scrollbar = None
        self.export_btn = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Entrada de semilla
        ttk.Label(input_frame, text="Semilla (4 dígitos):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.semilla_entry = ttk.Entry(input_frame)
        self.semilla_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Entrada de corridas
        ttk.Label(input_frame, text="Número de corridas:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.corridas_entry = ttk.Entry(input_frame)
        self.corridas_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Botón de generación
        generar_btn = ttk.Button(input_frame, text="Generar", command=self.generar_numeros)
        generar_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar expansión de columnas
        input_frame.columnconfigure(1, weight=1)
        
        # Frame para la tabla (inicialmente vacío)
        self.table_frame = ttk.Frame(main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
    
    def limpiar_tabla(self):
        """Elimina la tabla existente si hay una"""
        if self.tree:
            self.tree.destroy()
            self.tree = None
        if self.scrollbar:
            self.scrollbar.destroy()
            self.scrollbar = None
        if self.export_btn:
            self.export_btn.destroy()
            self.export_btn = None
    
    def generar_numeros(self):
        try:
            semilla = int(self.semilla_entry.get())
            corridas = int(self.corridas_entry.get())
            
            if not (1000 <= semilla <= 9999):
                messagebox.showerror("Error", "La semilla debe tener exactamente 4 dígitos")
                return
            
            resultados = generar_cuadrados_medios(semilla, corridas)
            self.mostrar_resultados(resultados)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def mostrar_resultados(self, resultados):
        # Limpiar tabla existente
        self.limpiar_tabla()
        
        # Crear Treeview (tabla)
        columns = ('iteracion', 'semilla', 'cuadrado', 'pseudoaleatorio', 'random_ri')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Configurar columnas
        self.tree.heading('iteracion', text='Iteración')
        self.tree.heading('semilla', text='Semilla (Xo)')
        self.tree.heading('cuadrado', text='Xo²')
        self.tree.heading('pseudoaleatorio', text='Pseudoaleatorio')
        self.tree.heading('random_ri', text='Random Ri')
        
        self.tree.column('iteracion', width=80, anchor=tk.CENTER)
        self.tree.column('semilla', width=100, anchor=tk.CENTER)
        self.tree.column('cuadrado', width=120, anchor=tk.CENTER)
        self.tree.column('pseudoaleatorio', width=120, anchor=tk.CENTER)
        self.tree.column('random_ri', width=100, anchor=tk.CENTER)
        
        # Insertar datos
        for res in resultados:
            self.tree.insert('', tk.END, values=(
                res['iteracion'],
                res['semilla'],
                res['cuadrado'],
                res['pseudoaleatorio'],
                f"{res['random_ri']:.4f}"
            ))
        
import sys
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Basado en la lógica del video Método de los cuadrados del medio en Python de Psyware
# URL: https://youtu.be/1wu_1HBEsas
# Se realizaron modificaciones/adaptaciones al código original.

# def generar_cuadrados_medios(semilla, corridas):
#     resultados = []
#     for i in range(corridas):
#         semilla_al_cuadrado = semilla * semilla
#         s = str(semilla_al_cuadrado).zfill(8)  # Rellenar con ceros hasta 8 dígitos
#         t = s[2:6]  # Tomar los 4 dígitos centrales
#         v = int(t)
#         r = v / 10000
#         resultados.append({
#             'iteracion': i,
#             'semilla': semilla,
#             'cuadrado': semilla_al_cuadrado,
#             'pseudoaleatorio': v,
#             'random_ri': r
#         })
#         semilla = v
#         if v == 0:
#             break
#     return resultados

# def generar_cuadrados_medios(semilla, corridas):
#     resultados = []
#     for i in range(corridas):
#         semilla_al_cuadrado = semilla * semilla
#         s = str(semilla_al_cuadrado)
#         largo = len(s)
        
#         # Lógica original para seleccionar dígitos
#         if largo == 8:
#             t = s[2:6]  # Toma 4 dígitos centrales para números de 8 dígitos
#         else:
#             t = s[1:5]  # Toma 4 dígitos desplazados para otros casos
            
#         v = int(t)
#         r = v / 10000
#         resultados.append({
#             'iteracion': i,
#             'semilla': semilla,
#             'cuadrado': semilla_al_cuadrado,
#             'pseudoaleatorio': v,
#             'random_ri': r
#         })
#         semilla = v
#         if v == 0:
#             break
#     return resultados

def generar_cuadrados_medios(semilla, corridas):
    resultados = []
    for i in range(corridas):
        semilla_al_cuadrado = semilla * semilla
        s = str(semilla_al_cuadrado)
        largo = len(s)
        
        # Lógica mejorada para selección de dígitos centrales
        if largo == 4:
            # Para exactamente 4 dígitos: tomar los 2 centrales
            t = s[1:3]
        elif largo > 4 and largo % 2 == 0:
            # Para pares mayores a 4: tomar 4 centrales
            centro = largo // 2
            t = s[centro-2:centro+2]
        elif largo % 2 == 1:
            # Para impares: tomar 3 centrales
            centro = largo // 2
            t = s[centro-1:centro+2]
        else:
            # Para longitudes menores a 4 (no debería ocurrir con semillas de 4 dígitos)
            t = s.zfill(4)[:2]  # Tomar primeros dígitos con relleno
            
        v = int(t)
        r = v / (10 ** len(t))  # Normalización dinámica
        resultados.append({
            'iteracion': i,
            'semilla': semilla,
            'cuadrado': semilla_al_cuadrado,
            'pseudoaleatorio': v,
            'random_ri': r
        })
        semilla = v
        if v == 0:
            break
    return resultados

def exportar_a_csv(resultados, filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            campos = ['iteracion', 'semilla', 'cuadrado', 'pseudoaleatorio', 'random_ri']
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writeheader()
            writer.writerows(resultados)
        return True
    except Exception as e:
        print(f"Error al exportar: {e}")
        return False

# Interfaz gráfica modificada
class GeneradorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Números Pseudoaleatorios")
        
        # Variables para controlar la tabla
        self.tree = None
        self.scrollbar = None
        self.export_btn = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles de entrada
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Entrada de semilla
        ttk.Label(input_frame, text="Semilla (4 dígitos):").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.semilla_entry = ttk.Entry(input_frame)
        self.semilla_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Entrada de corridas
        ttk.Label(input_frame, text="Número de corridas:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.corridas_entry = ttk.Entry(input_frame)
        self.corridas_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Botón de generación
        generar_btn = ttk.Button(input_frame, text="Generar", command=self.generar_numeros)
        generar_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Configurar expansión de columnas
        input_frame.columnconfigure(1, weight=1)
        
        # Frame para la tabla (inicialmente vacío)
        self.table_frame = ttk.Frame(main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
    
    def limpiar_tabla(self):
        """Elimina la tabla existente si hay una"""
        if self.tree:
            self.tree.destroy()
            self.tree = None
        if self.scrollbar:
            self.scrollbar.destroy()
            self.scrollbar = None
        if self.export_btn:
            self.export_btn.destroy()
            self.export_btn = None
    
    def generar_numeros(self):
        try:
            semilla = int(self.semilla_entry.get())
            corridas = int(self.corridas_entry.get())
            
            if not (1000 <= semilla <= 9999):
                messagebox.showerror("Error", "La semilla debe tener exactamente 4 dígitos")
                return
            
            resultados = generar_cuadrados_medios(semilla, corridas)
            self.mostrar_resultados(resultados)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def mostrar_resultados(self, resultados):
        # Limpiar tabla existente
        self.limpiar_tabla()
        
        # Crear Treeview (tabla)
        columns = ('iteracion', 'semilla', 'cuadrado', 'pseudoaleatorio', 'random_ri')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        
        # Configurar columnas
        self.tree.heading('iteracion', text='Iteración')
        self.tree.heading('semilla', text='Semilla (Xo)')
        self.tree.heading('cuadrado', text='Xo²')
        self.tree.heading('pseudoaleatorio', text='Pseudoaleatorio')
        self.tree.heading('random_ri', text='Random Ri')
        
        self.tree.column('iteracion', width=80, anchor=tk.CENTER)
        self.tree.column('semilla', width=100, anchor=tk.CENTER)
        self.tree.column('cuadrado', width=120, anchor=tk.CENTER)
        self.tree.column('pseudoaleatorio', width=120, anchor=tk.CENTER)
        self.tree.column('random_ri', width=100, anchor=tk.CENTER)
        
        # Insertar datos
        for res in resultados:
            self.tree.insert('', tk.END, values=(
                res['iteracion'],
                res['semilla'],
                res['cuadrado'],
                res['pseudoaleatorio'],
                f"{res['random_ri']:.4f}"
            ))
    
    def mostrar_resultados(self, resultados):
        # Limpiar tabla existente
        self.limpiar_tabla()
        
        # Contenedor para la tabla + scrollbar (usando pack)
        table_scroll_frame = ttk.Frame(self.table_frame)
        table_scroll_frame.pack(fill=tk.BOTH, expand=True)  # Se expande para ocupar espacio
        
        # Treeview (tabla)
        columns = ('iteracion', 'semilla', 'cuadrado', 'pseudoaleatorio', 'random_ri')
        self.tree = ttk.Treeview(table_scroll_frame, columns=columns, show='headings')
        
        # Configurar columnas (igual que antes)
        self.tree.heading('iteracion', text='Iteración')
        self.tree.heading('semilla', text='Semilla (Xo)')
        self.tree.heading('cuadrado', text='Xo²')
        self.tree.heading('pseudoaleatorio', text='Pseudoaleatorio')
        self.tree.heading('random_ri', text='Random Ri')
        
        self.tree.column('iteracion', width=80, anchor=tk.CENTER)
        self.tree.column('semilla', width=100, anchor=tk.CENTER)
        self.tree.column('cuadrado', width=120, anchor=tk.CENTER)
        self.tree.column('pseudoaleatorio', width=120, anchor=tk.CENTER)
        self.tree.column('random_ri', width=100, anchor=tk.CENTER)
        
        # Insertar datos
        for res in resultados:
            self.tree.insert('', tk.END, values=(
                res['iteracion'],
                res['semilla'],
                res['cuadrado'],
                res['pseudoaleatorio'],
                f"{res['random_ri']:.4f}"
            ))
        
        # Scrollbar (vertical, al lado derecho de la tabla)
        self.scrollbar = ttk.Scrollbar(table_scroll_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        
        # Posicionamiento con pack (tabla a la izquierda, scrollbar a la derecha)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botón Exportar (debajo de la tabla y scrollbar)
        self.export_btn = ttk.Button(
            self.table_frame,  # Se coloca en el frame principal, no en table_scroll_frame
            text="Exportar a CSV",
            command=lambda: self.exportar_resultados(resultados)
        )
        self.export_btn.pack(side=tk.BOTTOM, pady=10)  # Se ubica en la parte inferior