#libreries 
import tkinter as tk
import time 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import generateList, binarySearch, linealSearch


# Global variables
generatedList = []
size = 0
times_data = {"Lineal": [], "Binaria": []}
sizes_list = [100, 1000, 10000, 100000]

# Function to generate a list of random numbers and display it
def initializeList():
    global generatedList, size

    size = 0

    if var100.get() == 1:
        size = 100
    elif var1000.get() == 1:
        size = 1000
    elif var10k.get() == 1:
        size = 10000
    elif var100k.get() == 1:
        size = 100000
    
    if size > 0:
        generatedList = generateList(size)
        errorLabel.config(text=f"Lista generada de tamaño {size}")
    else:
        errorLabel.config(text="Please select a checkbox.")
        
    return

def searchNumber(searchType):

    global size, generatedList
    
    num_text = entry.get().strip()
    if not num_text.isdigit():
        errorLabel.config(text="Please enter a number.")
        return
    
    number = int(num_text)
    times = []

    if size > 0:

        if searchType == "bs":
            generatedList = sorted(generatedList)

        # Runs the search algorithm 5 times to calculate average time
        for i in range(5):
            start_time = time.perf_counter()
            if (searchType == "bs"):
                index = binarySearch(generatedList, number)
            
            else:
                index = linealSearch(generatedList, number)
            end_time = time.perf_counter()
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        avg_time = sum(times) / len(times)

        # Show results in the GUI
        if index == -1:
            resultLabel.config(text=f"Element not found in the list.")
        else:
            resultLabel.config(text=f"Element found in index:  {index}")

        timeLabel.config(text=f"Avg. time : {avg_time:.4f} ms")

        # Save for graphing
        if searchType == "ls":
            times_data["Lineal"].append(avg_time)
        else:
            times_data["Binaria"].append(avg_time)

        updateGraph()

    else:
        errorLabel.config(text="Please select a size.")
    
def updateGraph():
    # Solo graficar si hay datos
    if not times_data["Lineal"] or not times_data["Binaria"]:
        return

    ax.clear()
    ax.plot(sizes_list[:len(times_data["Lineal"])], times_data["Lineal"], marker='o', label="Lineal")
    ax.plot(sizes_list[:len(times_data["Binaria"])], times_data["Binaria"], marker='o', label="Binaria")
    ax.set_xlabel("Tamaño de lista")
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_title("Comparación de Búsquedas")
    ax.legend()
    canvas.draw()

# GUI setup

root = tk.Tk()
root.title("Act01 - Algoritmos de Búsqueda")
root.geometry("700x600")

# Labels for title and author

tk.Label(root, text="Actividad 01 - Algoritmos de Búsqueda", font=("Arial", 16)).pack(pady=5)
tk.Label(root, text="Arturo Morales Pedroza", font=("Arial", 14)).pack(pady=5)

errorLabel = tk.Label(root, text="", fg="red")
errorLabel.pack()

# Size options 

# Variables for checkboxes
var100 = tk.IntVar()
var1000 = tk.IntVar()
var10k = tk.IntVar()
var100k = tk.IntVar()

# Checkboxes for selecting list sizes

frame_size = tk.Frame(root)
frame_size.pack(pady=5)
tk.Checkbutton(frame_size, text="100", variable=var100).grid(row=0, column=1)
tk.Checkbutton(frame_size, text="1000", variable=var1000).grid(row=0, column=2)
tk.Checkbutton(frame_size, text="10k", variable=var10k).grid(row=0, column=3)
tk.Checkbutton(frame_size, text="100k", variable=var100k).grid(row=0, column=4)

tk.Button(root, text="Generate Numbers", command=initializeList).pack(pady=10)

tk.Label(root, text="Insert the number you're looking for").pack()
entry = tk.Entry(root)
entry.pack(pady=5)

#Seacrh buttons
tk.Button(root, text="Binary Search", command=lambda: searchNumber("bs")).pack(pady=5)
tk.Button(root, text="Lineal Search", command=lambda: searchNumber("ls")).pack(pady=5)

resultLabel = tk.Label(root, text="", font=("Arial", 12))
resultLabel.pack(pady=5)
timeLabel = tk.Label(root, text="", font=("Arial", 12))
timeLabel.pack(pady=5)

fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

root.mainloop()