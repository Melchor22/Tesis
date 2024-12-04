import time
import csv
from algoritmo_genetico import AlgoritmoGenetico

NUM_GENERACIONES = 100
NUM_INDIVIDUOS = 100
NUM_REQUISITOS = 100
NUM_PADRES = 10 #MAX = NUM_INDIVIDUOS/2
PROBABILIDAD_MUTA = 0.20
ALPHA = 0.71
NUM_EJECUCIONES = 30

#Archivo para guardar ejecuciones
archivo_ejecuciones = "ejecuciones.csv"

#Inicia conteo de tiempo de ejecución
inicio = time.time()

#Preparar encabezado del archivo CSV
with open(archivo_ejecuciones, mode='w', newline='') as archivo_csv:

    escritor = csv.writer(archivo_csv)
    escritor.writerow(["Ejecucion", "Generacion", "Mejor Aptitud"])

    for ejecucion in range (1, NUM_EJECUCIONES + 1):
        print(f"Ejecución {ejecucion} iniciada.")

        #Generación aleatoria de población inicial
        AlgoritmoGenetico.destroy_instance()
        AG = AlgoritmoGenetico(NUM_INDIVIDUOS, NUM_REQUISITOS)

        for generacion in range(NUM_GENERACIONES+1):
            print("Generación "+str(generacion))

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

            #Contar y mostrar en pantalla cuantos individuos son válidos
            contValido = sum(1 for solucion in AG.poblacion if solucion.esValido)
            print("Validos: "+str(contValido))

            #Mejor Solución
            mejor_aptitud = AG.poblacion[0].aptitud
            print("ID:"+str(AG.poblacion[0].id)+" Aptitud: "+str(mejor_aptitud))
            print()

            escritor.writerow([ejecucion, generacion, mejor_aptitud])

fin = time.time()
tiempo_ejecucion = fin - inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")