import math
import tkinter as tk
from tkinter import messagebox
import random

class Point: 
    def __init__(self, x ,y):
        self.x = x
        self.y = y


def spaceBeetwenAPair(point1, point2):
        distance = math.sqrt(math.pow((point1.x - point2.x), 2) + math.pow((point1.y - point2.y), 2 ))
        print(f"Distancia entre ({point1.x},{point1.y}) y ({point2.x},{point2.y}): {distance}")
        return distance

def findClosestDistance(points):
    min_distance = float('inf')
    closest_pair = (None, None)

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = spaceBeetwenAPair(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])


        print(f"Distancia mínima actual: {min_distance}")

    return closest_pair, min_distance

# ---------- GUI ------------
root = tk.Tk()
root.title("Partc. 05 Fuerza bruta")
root.geometry("900x650")

# Marco para entradas
entradas_frame = tk.Frame(root)
entradas_frame.pack(pady=10)

tk.Label(entradas_frame, text="x").grid(row=0, column=1, padx=5)
tk.Label(entradas_frame, text="y").grid(row=0, column=2, padx=5)

entries = []

for i in range(5):
    tk.Label(entradas_frame, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5, pady=2)
    x_entry = tk.Entry(entradas_frame, width=5)
    y_entry = tk.Entry(entradas_frame, width=5)
    x_entry.grid(row=i+1, column=1, padx=5)
    y_entry.grid(row=i+1, column=2, padx=5)
    entries.append((x_entry, y_entry))

# Canvas para graficar
canvas = tk.Canvas(root, bg="white", width=600, height=400)
canvas.pack(pady=10)

points_list = []

def draw_points(points):
    canvas.delete("all")
    for p in points:
        # invertimos eje Y para que (0,0) sea abajo-izq si quieres
        x, y = p.x, p.y
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="blue")
    if len(points) >= 2:
        # Dibuja la línea del par más cercano
        closest_pair, dist = findClosestDistance(points)
        if closest_pair[0] and closest_pair[1]:
            canvas.create_line(closest_pair[0].x, closest_pair[0].y,
                               closest_pair[1].x, closest_pair[1].y,
                               fill="red", width=2)

def calcular():
    global points_list
    points_list = []
    try:
        for x_e, y_e in entries:
            x = float(x_e.get())
            y = float(y_e.get())
            points_list.append(Point(x, y))
    except ValueError:
        messagebox.showerror("Error", "Introduce solo números en x e y")
        return
    if len(points_list) < 2:
        messagebox.showinfo("Info", "Se necesitan al menos 2 puntos")
        return
    draw_points(points_list)
    par, dist = findClosestDistance(points_list)
    messagebox.showinfo("Resultado", 
                        f"Par más cercano: ({par[0].x},{par[0].y}) y ({par[1].x},{par[1].y})\nDistancia: {dist:.2f}")

def random_fill():
    for x_e, y_e in entries:
        x = random.randint(20, 580)
        y = random.randint(20, 380)
        x_e.delete(0, tk.END)
        y_e.delete(0, tk.END)
        x_e.insert(0, str(x))
        y_e.insert(0, str(y))

def limpiar():
    for x_e, y_e in entries:
        x_e.delete(0, tk.END)
        y_e.delete(0, tk.END)
    canvas.delete("all")
    points_list.clear()

# Botones
botones_frame = tk.Frame(root)
botones_frame.pack(pady=5)

tk.Button(botones_frame, text="Calcular", command=calcular, width=10).grid(row=0, column=0, padx=5)
tk.Button(botones_frame, text="Random", command=random_fill, width=10).grid(row=0, column=1, padx=5)
tk.Button(botones_frame, text="Limpiar", command=limpiar, width=10).grid(row=0, column=2, padx=5)

root.mainloop()

