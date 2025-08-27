#librerias
import random as rd
import tkinter as tk
import time
import matplotlib.pyplot as plt

#globales
lista = []
vectorquick = []
vectorbs = []
vectormerge = []
size = 0 
times_data = {"bubble": [], "merge": [], "quick": []}
cant_datos = []

#-----------generar lista ---------------

def generateList():

    global lista, size, vectorquick, vectorbs, vectormerge, times_data, cant_datos

    size += 50  # aumenta de 50 en 50
    lista = [rd.randint(0, size) for _ in range(size)]

    vectorquick = lista.copy()
    vectorbs = lista.copy()
    vectormerge = lista.copy()

    print(f"Se generó una lista de {size} elementos")
    print(lista)

    #bubble sort
    start_time = time.perf_counter()
    bubblesort(vectorbs)
    end_time = time.perf_counter()
    average_time = (end_time - start_time) * 1000  # Convert to milliseconds
    times_data["bubble"].append(average_time)

    #merge sort
    start_time = time.perf_counter()
    mergesort(vectormerge)
    end_time = time.perf_counter()
    average_time = (end_time - start_time) * 1000  # Convert to milliseconds
    times_data["merge"].append(average_time)

    #quick sort
    start_time = time.perf_counter()
    quicksort(vectorquick)
    end_time = time.perf_counter()
    average_time = (end_time - start_time) * 1000  # Convert to milliseconds
    times_data["quick"].append(average_time)

    cant_datos.append(size)

#------------Metodos ordenamiento--------------

def bubblesort(lista):

    """Esta función ordenara el vector que le pases como argumento con el Método de Bubble Sort"""
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar es (bubble):",lista)
    n = 0 # Establecemos un contador del largo del vector
    
    for _ in lista:
        n += 1 #Contamos la cantidad de caracteres dentro del vector
    
    for i in range(n-1): 
    # Le damos un rango n para que complete el proceso. 
        for j in range(0, n-i-1): 
            # Revisa la matriz de 0 hasta n-i-1
            if lista[j] > lista[j+1] :
                lista[j], lista[j+1] = lista[j+1], lista[j]
            # Se intercambian si el elemento encontrado es mayor 
            # Luego pasa al siguiente
    print ("La lista  ordenado es: ",lista)

def mergesort(vectormerge): 
    """Esta función ordenara el vector que le pases como argumento 
    con el Método Merge Sort"""
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar con merge es:", vectormerge)
    
    def merge(vectormerge):
    
        def largo(vec):
                largovec = 0 # Establecemos un contador del largovec
                for _ in vec:
                    largovec += 1 # Obtenemos el largo del vector
                return largovec
        
        
        if largo(vectormerge) >1: 
            medio = largo(vectormerge)//2 # Buscamos el medio del vector
            
            # Lo dividimos en 2 partes 
            izq = vectormerge[:medio]  
            der = vectormerge[medio:]
            
            merge(izq) # Mismo procedimiento a la primer mitad
            merge(der) # Mismo procedimiento a la segunda mitad
            
            i = j = k = 0
            
            # Copiamos los datos a los vectores temporales izq[] y der[] 
            while i < largo(izq) and j < largo(der): 
                if izq[i] < der[j]: 
                    vectormerge[k] = izq[i] 
                    i+= 1
                else: 
                    vectormerge[k] = der[j] 
                    j+= 1
                k += 1
            
            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda 
            while i < largo(izq): 
                vectormerge[k] = izq[i] 
                i+= 1
                k+= 1
            
            while j < largo(der): 
                vectormerge[k] = der[j] 
                j+= 1
                k+= 1
    merge(vectormerge)
    print("El vector ordenado con merge es: ", vectormerge)

def quicksort(vectorquick, start = 0, end = len(vectorquick) - 1 ):
    
    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar con quick es:", vectorquick)
    
    def quick(vectorquick, start = 0, end = len(vectorquick) - 1):
        
        
        if start >= end:
            return

        def particion(vectorquick, start = 0, end = len(vectorquick) - 1):
            pivot = vectorquick[start]
            menor = start + 1
            mayor = end

            while True:
                # Si el valor actual es mayor que el pivot
                # está en el lugar correcto (lado derecho del pivot) y podemos 
                # movernos hacia la izquierda, al siguiente elemento.
                # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica 
                # que ya hemos movido todos los elementos a su lado correcto del pivot
                while menor <= mayor and vectorquick[mayor] >= pivot:
                    mayor = mayor - 1

                # Proceso opuesto al anterior            
                while menor <= mayor and vectorquick[menor] <= pivot:
                    menor = menor + 1

                # Encontramos un valor sea mayor o menor y que este fuera del arreglo
                # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
                if menor <= mayor:
                    vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
                    # Continua el bucle
                else:
                    # Salimos del bucle
                    break

            vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]
            
            return mayor
        
        p = particion(vectorquick, start, end)
        quick(vectorquick, start, p-1)
        quick(vectorquick, p+1, end)
        
    quick(vectorquick)
    print("El vector ordenado con quick es:", vectorquick)

#-------------graficar----------------
def updateGraph():
    # Solo graficar si hay datos
    if not times_data["bubble"] or not times_data["merge"] or not times_data["quick"]:
        return

    ax.clear()
    ax.plot(cant_datos, times_data["bubble"], marker='o', label="Bubble")
    ax.plot(cant_datos, times_data["merge"], marker='o', label="Merge")
    ax.plot(cant_datos, times_data["quick"], marker='o', label="Quick")
    ax.set_xlabel("Size")
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_title("Comparación de ordenamientos")
    ax.legend()
    plt.show()

    
#-------------ventana------------

root = tk.Tk()
root.title("Participacion - Complejidad Temporal")
root.geometry("350x200")

# Labels for title and author

tk.Label(root, text="Participacion - Complejidad Temporal", font=("Arial", 16)).pack(pady=5)


tk.Button(root, text="Generate Numbers", command=generateList).pack(pady=10)

tk.Button(root, text="Update Graph", command=updateGraph).pack(pady=10)

fig, ax = plt.subplots(figsize=(6,4))

root.mainloop()


