import time
from algoritmo_genetico import AlgoritmoGenetico

NUM_GENERACIONES = 100
NUM_INDIVIDUOS = 100
NUM_REQUISITOS = 100
NUM_PADRES = 50  # MAX = NUM_INDIVIDUOS / 2
PROBABILIDAD_MUTA = 0.5
NUM_MUTACIONES = 10
ALPHA = 0.6

# Inicia conteo de tiempo de ejecución
inicio = time.time()

# Generación aleatoria de población inicial
AG = AlgoritmoGenetico(NUM_INDIVIDUOS, NUM_REQUISITOS)

for i in range(NUM_GENERACIONES + 1):
    print("Generación " + str(i))

    # Cálculo de Aptitud de la Población en GPU
    AG.calcularAptitud(ALPHA)

    # Cruza y Muta en GPU
    hijos = AG.cruza(NUM_PADRES)
    AG.mutacion(hijos, PROBABILIDAD_MUTA, NUM_MUTACIONES)
    AG.calcularAptitud(ALPHA, hijos)

    # Reemplazar Población en GPU
    AG.reemplazarPoblacion(hijos)

    # Ordenar Población Según Aptitud en GPU
    AG.ordenarSegunAptitud()

    # Ordenar Soluciones Válidas en GPU
    validosOrdenados = AG.ordenarValidos()

    # Contar y mostrar en pantalla cuántos individuos son válidos
    # Usamos operaciones en GPU para el conteo
    contValido = sum(1 for solucion in AG.poblacion if solucion.esValido)
    print("Validos: " + str(contValido))

    # Mejor Solución (se mantiene igual)
    print("ID:" + str(AG.poblacion[0].id) + " Aptitud: " + str(AG.poblacion[0].aptitud))
    print()

# Termina el conteo de tiempo de ejecución
fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")
