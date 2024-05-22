from mpi4py import MPI
import numpy as np
import time


def particion(arreglo, menor, high):
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
        pivot_idx = particion(arreglo, menor, high)
        if pivot_idx == k:
            return arreglo[pivot_idx]
        elif pivot_idx < k:
            return quickselect(arreglo, pivot_idx + 1, high, k)
        else:
            return quickselect(arreglo, menor, pivot_idx - 1, k)

# Inicialización de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Proceso raíz
if rank == 0:
    arreglo = np.random.randint(0, 1000000000, size=1000000000)
else:
    arreglo = None

# Compartir el arreglo entre los procesos
arreglo = comm.bcast(arreglo, root=0)

# Calcular cuántos elementos debe manejar cada proceso
local_size = len(arreglo) // size
local_arr = np.empty(local_size, dtype=int)

# Dividir el arreglo en partes iguales entre los procesos
comm.Scatter(arreglo, local_arr, root=0)

# Calcular el enésimo elemento más pequeño localmente
k = 5
inicial = time.time()
kth_smallest_local = quickselect(local_arr, 0, len(local_arr) - 1, k)
tiempofinal = time.time()

# Recopilar los resultados parciales
resultado = comm.gather(kth_smallest_local, root=0)

# En el proceso raíz, encontrar el enésimo elemento más pequeño global
if rank == 0:
    kth_smallest_global = min(resultado)
    print(f"El {k} elemento más pequeño es: {kth_smallest_global}")
    print("Tiempo de ejecución:", tiempofinal - inicial, "segundos")


