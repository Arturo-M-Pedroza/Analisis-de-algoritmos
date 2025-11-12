import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import equipoHuffman as huffman
import nsm
import pickle
from bitstring import BitArray, ConstBitStream
from bitarray import bitarray

contenido_bin = None
diccionario_h = None

def compress_string():
    adn_Chain = nsm.obtener_secuencia_ncbi(entry_chain.get().strip())
    pattern = entry_pattern.get().strip()
    
    diccionario_h = huffman.huffman_encoding(adn_Chain)
    print(diccionario_h)
    compress_adn_chain = huffman.compresion(adn_Chain, diccionario_h)
    compress_pattern = huffman.compresion(pattern, diccionario_h)

    print("=== Cadena Comprimida ===")
    print(compress_adn_chain)

    print("=== Patrón Comprimido ===")
    print(compress_pattern)

    print("\n=== Búsqueda Naive ===")
    resultados_naive = nsm.naive_search(compress_adn_chain, compress_pattern)
    print(f"Coincidencias encontradas: {len(resultados_naive)} \n en posiciones: {resultados_naive}")


def unzip_files():
    global contenido_bin, diccionario_h

    comprimido = BitArray(bin=contenido_bin.to01())
    print(diccionario_h)
    contenido = huffman.descompresion(comprimido, diccionario_h)
    print(type(contenido))

#-------------
#Main window 
#-------------

root = tk.Tk()
root.title("Algoritmo de Huffman (Proyecto)")
root.geometry("300x200")

tk.Label(root, text="Ingrese la cadena de bases a buscar").pack()
entry_pattern = tk.Entry(root)
entry_pattern.pack(pady=5)

tk.Label(root, text="Ingrese el id del adn donde se quiere buscar buscar").pack()
entry_chain = tk.Entry(root)
entry_chain.pack(pady=5)

tk.Button(root, text="Buscar", command=compress_string).pack(pady=5)

root.mainloop()
