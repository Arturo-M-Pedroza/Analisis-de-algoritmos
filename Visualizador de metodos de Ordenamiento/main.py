import tkinter as tk
from tkinter import ttk
import random, time
import time
import matplotlib.pyplot as plt

# ---------------------------
# Parámetros generales
# ---------------------------
ANCHO = 800
ALTO = 300
N_BARRAS = 40
VAL_MIN, VAL_MAX = 5, 100
times_data = {
    "bubble": {"sizes": [], "times": []},
    "merge": {"sizes": [], "times": []},
    "quick": {"sizes": [], "times": []},
    "selection": {"sizes": [], "times": []}
}

# ---------------------------
# Algoritmos paso a paso
# ---------------------------
def selection_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx])
            yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx])
        yield
    draw_callback(activos=[])

def bubblesort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            draw_callback(activos=[j, j + 1])
            yield
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_callback(activos=[j, j + 1])
                yield
        yield
    draw_callback(activos=[])

def mergesort_steps(data, draw_callback): 
    def merge(data):
        def largo(vec):
                largovec = 0 # Establecemos un contador del largovec
                for _ in vec:
                    largovec += 1 # Obtenemos el largo del vector
                return largovec
            
        if largo(data) >1: 
            medio = largo(data)//2 # Buscamos el medio del vector
            
            # Lo dividimos en 2 partes 
            izq = data[:medio]  
            der = data[medio:]
            
            yield from merge(izq) # Use yield from for recursion
            yield from merge(der) # Use yield from for recursion
            
            i = j = k = 0
            
            # Copiamos los datos a los vectores temporales izq[] y der[] 
            while i < largo(izq) and j < largo(der): 
                if izq[i] < der[j]:
                    data[k] = izq[i] 
                    i+= 1
                    draw_callback(activos=[k])
                    yield 
                else:
                    data[k] = der[j] 
                    j+= 1
                    draw_callback(activos=[k])
                    yield 
                k += 1
                draw_callback(activos=[k])
                yield 
            
            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda 
            while i < largo(izq):
                data[k] = izq[i] 
                i+= 1
                k+= 1
                draw_callback(activos=[k])
                yield  
            
            while j < largo(der):
                data[k] = der[j] 
                j+= 1
                k+= 1
                draw_callback(activos=[k])
                yield  
    yield from merge(data)


def quicksort_steps(data, draw_callback):
    def quick(data, start = 0, end = len(data) - 1):
        if start >= end:
            return
        def particion(data, start = 0, end = len(data) - 1):
            pivot = data[start]
            menor = start + 1
            mayor = end
            while True:
                # Si el valor actual es mayor que el pivot
                # está en el lugar correcto (lado derecho del pivot) y podemos 
                # movernos hacia la izquierda, al siguiente elemento.
                # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica 
                # que ya hemos movido todos los elementos a su lado correcto del pivot
                while menor <= mayor and data[mayor] >= pivot:
                    mayor = mayor - 1
                    draw_callback(activos=[mayor, menor, start])
                    yield 

                # Proceso opuesto al anterior            
                while menor <= mayor and data[menor] <= pivot:
                    menor = menor + 1
                    draw_callback(activos=[mayor, menor, start])
                    yield 

                # Encontramos un valor sea mayor o menor y que este fuera del arreglo
                # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
                if menor <= mayor:
                    data[menor], data[mayor] = data[mayor], data[menor]
                    # Continua el bucle
                else:
                    # Salimos del bucle
                    break

            data[start], data[mayor] = data[mayor], data[start]
            return mayor
        p = yield from particion(data, start, end)
        draw_callback(activos=[p])
        yield from quick(data, start, p-1)
        draw_callback(activos=[p])
        yield from quick(data, p+1, end)
    yield from quick(data)
    print("El vector ordenado con quick es:", data)


# ---------------------------
# Clase principal
# ---------------------------
class Visualizador:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador - Ordenamiento")

        self.datos = []

        # Canvas
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="white")
        self.canvas.pack(padx=10, pady=10)

        # Panel de controles
        panel = tk.Frame(root)
        panel.pack(pady=6)

        self.combo = ttk.Combobox(panel, values=["Selection Sort", "Bubble Sort", "Merge Sort", "Quick Sort"])
        self.combo.current(0)
        self.combo.grid(row=0, column=0, columnspan=2, padx=5, pady=2) # columnspan para abarcar 2 columnas

        tk.Label(panel, text="Retraso (ms)").grid(row=0, column=2, padx=5, pady=2, sticky="e")
        self.velocimetro = tk.Scale(panel, from_=1, to=200, orient="horizontal")
        self.velocimetro.set(50)  # valor inicial
        self.velocimetro.grid(row=0, column=3, columnspan=2, padx=5, pady=2) # columnspan para abarcar 2 columnas
        
        # --- Fila 1 ---
        tk.Label(panel, text="Cantidad de Barras:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.entry_barras = tk.Entry(panel, width=10)
        self.entry_barras.grid(row=1, column=1, padx=5, pady=5)
        self.entry_barras.insert(0, str(N_BARRAS)) # Inserta el valor por defecto

        tk.Button(panel, text="Generar", command=self.generar).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(panel, text="Ordenar", command=self.ordenar).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(panel, text="Mezclar", command=self.mezclar).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(panel, text="Graficar", command=self.updateGraph).grid(row=1, column=5, padx=5, pady=5)
        tk.Button(panel, text="Limpiar", command=self.limpiar_tiempos).grid(row=1, column=6, padx=5, pady=5)

        # Estado inicial
        self.generar()

    # ---------------------------
    # Métodos
    # ---------------------------
    def dibujar_barras(self, activos=None):
        self.canvas.delete("all")
        if not self.datos:
            return
        n = len(self.datos)
        margen = 10
        ancho_disp = ANCHO - 2 * margen
        alto_disp = ALTO - 2 * margen
        w = ancho_disp / n
        esc = alto_disp / max(self.datos)

        for i, v in enumerate(self.datos):
            x0 = margen + i * w
            x1 = x0 + w * 0.9
            h = v * esc
            y0 = ALTO - margen - h
            y1 = ALTO - margen

            color = "#4e79a7"
            if activos and i in activos:
                color = "#f28e2b"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self.canvas.create_text(6, 6, anchor="nw", text=f"n={len(self.datos)}", fill="#666")

    def generar(self):
        random.seed(time.time())
        try:
            n_barras = int(self.entry_barras.get())
        except ValueError:
            # Si el valor no es un número válido, usa un valor por defecto (40)
            n_barras = 40
            self.entry_barras.delete(0, tk.END)
            self.entry_barras.insert(0, str(n_barras))
            
        # Usa la nueva variable 'n_barras' para crear la lista
        self.datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(n_barras)]
        self.dibujar_barras()
    
    def limpiar_tiempos(self):

        for key in times_data:
            times_data[key]["sizes"].clear()
            times_data[key]["times"].clear()
        
        self.dibujar_barras()


    def mezclar(self):
        # Mezcla aleatoriamente la lista de datos actual.
        if self.datos:
            random.shuffle(self.datos)
            self.dibujar_barras() # Vuelve a dibujar las barras en su nuevo orden
            print("Datos mezclados:", self.datos)

    def ordenar(self):

        self.start_time = time.perf_counter()
        algoritmo = self.combo.get()

        # Copia los datos para que la animación no afecte la lista original instantáneamente
        datos_copia = self.datos[:]

        if algoritmo == "Selection Sort":
            gen = selection_sort_steps(datos_copia, self.dibujar_barras)
        elif algoritmo == "Merge Sort":
            gen = mergesort_steps(datos_copia, self.dibujar_barras)
        elif algoritmo == "Bubble Sort":
            gen = bubblesort_steps(datos_copia, self.dibujar_barras)
        elif algoritmo == "Quick Sort":
            gen = quicksort_steps(datos_copia, self.dibujar_barras)
        else:
            print("Error: algoritmo no implementado")
            return
    
    

        def paso():
            try:
                next(gen)
                self.datos = datos_copia # Actualiza los datos en cada paso
                velocidad = self.velocimetro.get()  # usa el valor del slider
                self.root.after(velocidad, paso)
            except StopIteration:
                # La animación terminó. Ahora detenemos el cronómetro.
                end_time = time.perf_counter()
                duracion_ms = ((end_time - self.start_time) * 1000) / self.velocimetro.get()  # Duración en ms ajustada por velocidad

                # Diccionario para mapear nombres a claves
                algo_map = {
                    "Selection Sort": "selection",
                    "Bubble Sort": "bubble",
                    "Merge Sort": "merge",
                    "Quick Sort": "quick"
                }

                # Obtener la clave correcta
                key = algo_map.get(algoritmo)
                if key:
                    # Guarda el tiempo y el tamaño correspondiente
                    times_data[key]["times"].append(duracion_ms)
                    times_data[key]["sizes"].append(self.entry_barras.get())
                    print(times_data)  # Muestra los datos almacenados
                
                print(f"Tiempo para {algoritmo}: {duracion_ms:.2f} ms")
                self.dibujar_barras() # Dibuja el estado final
                
        paso()

    #-------------graficar----------------
    def updateGraph(self):

         # Verifica que haya datos para graficar
        has_data = any(d["times"] for d in times_data.values())
        if not has_data:
            print("No hay datos suficientes para graficar.")
            return
    
        fig, ax = plt.subplots(figsize=(6,4))

        # Grafica cada algoritmo usando sus propios datos de tamaño y tiempo
        ax.plot(times_data["bubble"]["sizes"], times_data["bubble"]["times"], marker='o', linestyle='--', label="Bubble", color='red')
        ax.plot(times_data["merge"]["sizes"], times_data["merge"]["times"], marker='o', linestyle='--', label="Merge", color='green')
        ax.plot(times_data["quick"]["sizes"], times_data["quick"]["times"], marker='o', linestyle='--', label="Quick", color='blue')
        ax.plot(times_data["selection"]["sizes"], times_data["selection"]["times"], marker='o', linestyle='--', label="Selection", color='purple') # Etiqueta corregida

        ax.set_xlabel("Cantidad de Datos (N)")
        ax.set_ylabel("Tiempo (ms)")
        ax.set_title("Comparación de Tiempos de Ordenamiento")
        ax.legend()
        plt.show()


# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Visualizador(root)
    root.mainloop()

