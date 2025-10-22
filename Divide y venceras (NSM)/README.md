# Búsqueda de Patrones en Secuencias de ADN: Naive vs. Divide y Vencerás

Este proyecto implementa y compara dos algoritmos de búsqueda de cadenas (`Naive Search` y `Divide and Conquer Search`) para encontrar un patrón de ADN específico dentro de una secuencia genética. La secuencia de ADN (genoma del SARS-CoV-2) se obtiene directamente de la base de datos del **NCBI** (National Center for Biotechnology Information) utilizando la librería Biopython.

El objetivo principal es analizar y visualizar la diferencia de rendimiento entre un enfoque de fuerza bruta y uno basado en la técnica de "divide y vencerás".

## Características Principales

* **Conexión con NCBI**: Descarga secuencias de nucleótidos directamente desde la base de datos de NCBI usando un identificador de secuencia.
* **Algoritmo Naive**: Implementación del algoritmo clásico de búsqueda de fuerza bruta.
* **Algoritmo Divide y Vencerás**: Una adaptación del paradigma "divide y vencerás" para la búsqueda de patrones.
* **Medición de Rendimiento**: Mide y compara el tiempo de ejecución de ambos algoritmos en subconjuntos de datos de tamaño creciente.
* **Visualización de Resultados**: Genera una gráfica comparativa del rendimiento utilizando `matplotlib` para una fácil interpretación de los resultados.

## Requisitos

Para ejecutar este proyecto, necesitarás tener instalado:

* Python 3.x
* Librería `biopython`
* Librería `matplotlib`
  
##  Uso

El script realizará las siguientes acciones de forma automática:

1.  **Descargará** la secuencia del genoma del SARS-CoV-2 (`NC_045512.2`) desde NCBI.
2.  **Ejecutará** la búsqueda del patrón `ATGTTTGTTT` utilizando el algoritmo Naive y mostrará las posiciones encontradas.
3.  **Ejecutará** la búsqueda con el algoritmo de Divide y Vencerás y mostrará sus resultados.
4.  **Medirá** los tiempos de ejecución para ambos algoritmos en fragmentos de la secuencia de distintos tamaños.
5.  **Mostrará** una gráfica comparando el rendimiento de ambos.

## Funcionamiento de los Algoritmos

### Búsqueda Naive (Fuerza Bruta)

Este es el enfoque más directo. El algoritmo recorre el texto principal de izquierda a derecha, y en cada posición, comprueba si el patrón coincide con el subtexto correspondiente. Su complejidad temporal en el peor de los casos es de $O((n-m+1) \cdot m)$, donde $n$ es la longitud del texto y $m$ es la longitud del patrón.

### Búsqueda Divide y Vencerás

Esta implementación adapta el paradigma "divide y vencerás" de la siguiente manera:

1.  **Caso Base**: Si el texto es demasiado corto para contener el patrón, la búsqueda termina. Si es de un tamaño manejable, se aplica una búsqueda directa.
2.  **Dividir**: Si el texto es grande, se divide aproximadamente por la mitad.
3.  **Conquistar**: Se llama recursivamente a la función de búsqueda en la mitad izquierda y en la mitad derecha.
    * Para no perder coincidencias que puedan cruzar el punto de división, la búsqueda en la mitad izquierda se extiende `m-1` caracteres hacia la derecha.
4.  **Combinar**: Los resultados de ambas llamadas recursivas se combinan en una sola lista de resultados.

## Salida Esperada

Al ejecutar el script, verás en la consola la confirmación de la descarga y los resultados de ambas búsquedas.

```
Descargando secuencia NC_045512.2 desde NCBI...
Secuencia descargada: 29903 bases.

=== Búsqueda Naive ===
Coincidencias encontradas: 3 
 en posiciones: [1343, 10523, 22823]

=== Búsqueda Divide y Vencerás ===
Coincidencias encontradas: 3 
 en posiciones: [1343, 10523, 22823]
```

Finalmente, se abrirá una ventana con una gráfica similar a esta, mostrando la comparativa de tiempos:

---

**Autor:** Arturo Morales Pedroza
