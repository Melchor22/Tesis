import time
from algoritmo_genetico import AlgoritmoGenetico

NUM_GENERACIONES = 100
NUM_INDIVIDUOS = 100
NUM_REQUISITOS = 100
NUM_PADRES = 10 #MAX = NUM_INDIVIDUOS/2
PROBABILIDAD_MUTA = 0.20
NUM_MUTACIONES = 1
ALPHA = 0.71

#Inicia conteo de tiempo de ejecución
inicio = time.time()

#Generación aleatoria de población inicial
AG = AlgoritmoGenetico(NUM_INDIVIDUOS, NUM_REQUISITOS)

for i in range(NUM_GENERACIONES+1):
    print("Generación "+str(i))

    #Calculo de Aptitud de Población
    AG.calcularAptitud(ALPHA)

    #Cruza y Muta
    hijos = AG.cruza(NUM_PADRES)
    AG.mutacion(hijos, PROBABILIDAD_MUTA)
    AG.calcularAptitud(ALPHA, hijos)

    #Reemplazar Poblacion
    AG.reemplazarPoblacion(hijos)

    #Ordenar Población Segun Aptitud
    AG.ordenarSegunAptitud()

    #Ordenar Soluciones Válidas
    validosOrdenados = AG.ordenarValidos()

    #Contar y mostrar en pantalla cuantos individuos son válidos
    contValido = 0
    for solucion in AG.poblacion:
        if (solucion.esValido):
            contValido += 1
    print("Validos: "+str(contValido))

    #Mejor Solución
    print("ID:"+str(AG.poblacion[0].id)+" Aptitud: "+str(AG.poblacion[0].aptitud))
    print()

fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")