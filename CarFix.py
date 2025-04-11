import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CarFix:
    def __init__(self, root):
        self.root = root
        self.root.title("CarFix: Gestión de Deliverys")
        self.root.geometry("800x600")
        
        
        self.clientes = self._generar_clientes(1000)
        self.tamanos = [100, 250, 500, 750, 1000]
        
        
        self._crear_interfaz()
    
    def _generar_clientes(self, cantidad):
       
        return [
            {
                'id': random.randint(1000, 9999),
                'orden_pedido': random.randint(1, 100),
                'distancia': random.randint(1, 25),  
                'tiempo_exigido': random.randint(8,20 ),  
                'tiempo_entrega': random.randint(10, 30),  
                'nombre': f"Cliente {random.randint(1, 1000)}"
            }
            for _ in range(cantidad)
        ]
    
    def _ordenar_por_pedido(self, clientes):
       
        return sorted(clientes, key=lambda x: x['orden_pedido'])
    
    def _ordenar_por_distancia(self, clientes):
       
        return sorted(clientes, key=lambda x: x['distancia'])
    
    def _ordenar_por_tiempo_exigido(self, clientes):
       
        return sorted(clientes, key=lambda x: x['tiempo_exigido'])
    
    def _medir_rendimiento(self):
       
        algoritmos = [
            ("Ordenar por Pedido", self._ordenar_por_pedido),
            ("Ordenar por Distancia", self._ordenar_por_distancia),
            ("Ordenar por Tiempo Exigido", self._ordenar_por_tiempo_exigido)
        ] 
        
        resultados = {nombre: [] for nombre, _ in algoritmos}
        
        for size in self.tamanos:
            subconjunto = self.clientes[:size]
            
            for nombre, algoritmo in algoritmos:
                datos_copia = subconjunto.copy()
                
                inicio = time.time()
                algoritmo(datos_copia)
                fin = time.time()
                
                resultados[nombre].append(fin - inicio)
        
        return resultados
    
    def _crear_interfaz(self):
        
        frame_principal = ttk.Frame(self.root, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame_principal, 
            text="CarFix: Análisis de Algoritmos de Delivery", 
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        
        botones = [
            ("Analizar Rendimiento", self._mostrar_grafica),
            ("Ver Ejemplo de Datos", self._mostrar_ejemplo_datos),
            ("Ayuda", self._mostrar_ayuda)
        ]
        
        for texto, comando in botones:
            ttk.Button(
                frame_botones, 
                text=texto, 
                command=comando
            ).pack(side=tk.LEFT, padx=10)
        
        self.frame_grafica = ttk.Frame(frame_principal)
        self.frame_grafica.pack(fill=tk.BOTH, expand=True)
    
    def _mostrar_grafica(self):
       
        for widget in self.frame_grafica.winfo_children():
            widget.destroy()
        
        resultados = self._medir_rendimiento()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for nombre, tiempos in resultados.items():
            ax.plot(self.tamanos, tiempos, marker='o', label=nombre)
        
        ax.set_title('Rendimiento de Algoritmos en CarFix')
        ax.set_xlabel('Número de Clientes')
        ax.set_ylabel('Tiempo de Ejecución (segundos)')
        ax.legend()
        ax.grid(True)
        
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    
    def _mostrar_ejemplo_datos(self):
      
        mensaje = "\n".join([
            f"ID: {c['id']}, Pedido: {c['orden_pedido']}, Distancia: {c['distancia']} km, "
            f"Tiempo Exigido: {c['tiempo_exigido']} min, Entrega: {c['tiempo_entrega']} min"
            for c in self.clientes[:5]
        ])
        
        messagebox.showinfo("Ejemplo de Datos", mensaje)
    
    def _mostrar_ayuda(self):
        
        ayuda = (
            "CarFix: Gestión de Deliverys\n\n"
            "Funciones:\n"
            "- Analizar Rendimiento: Compara velocidad de algoritmos.\n"
            "- Ver Ejemplo de Datos: Muestra datos simulados.\n"
            "- Ayuda: Información del sistema.\n\n"
            "Algoritmos:\n"
            "1. Pedido: Organiza por orden de solicitud.\n"
            "2. Distancia: Optimiza rutas según distancia.\n"
            "3. Tiempo Exigido: Prioriza tiempos críticos."
        )
        messagebox.showinfo("Ayuda", ayuda)

def main():
   
    root = tk.Tk()
    CarFix(root)
    root.mainloop()


if __name__ == "__main__":
    main()
