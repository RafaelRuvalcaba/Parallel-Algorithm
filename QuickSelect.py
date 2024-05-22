import numpy as np
import time

def partition(arreglo, menor, high):
    pivote = arreglo[high]
    i = menor - 1
    for j in range(menor, high):
        if arreglo[j] <= pivote:
            i += 1
            arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
    arreglo[i + 1], arreglo[high] = arreglo[high], arreglo[i + 1]
    return i + 1

def quickselect(arreglo, menor, high, k):
    if menor <= high:
        pivot_idx = partition(arreglo, menor, high)
        if pivot_idx == k:
            return arreglo[pivot_idx]
        elif pivot_idx < k:
            return quickselect(arreglo, pivot_idx + 1, high, k)
        else:
            return quickselect(arreglo, menor, pivot_idx - 1, k)

# Generar datos aleatorios
arreglo = np.random.randint(0, 100000000, size=100000000)

# Calcular el enésimo elemento más pequeño
k = 5
inicial = time.time()
kth_smallest = quickselect(arreglo, 0, len(arreglo) - 1, k)
tiempofinal = time.time()

print(f"El {k}º elemento más pequeño es: {kth_smallest}")
print("Tiempo de ejecución:", tiempofinal - inicial, "segundos")
