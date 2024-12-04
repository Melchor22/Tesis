import random
import numpy as np
from solucion import Solucion

class AlgoritmoGenetico:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AlgoritmoGenetico, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def destroy_instance(cls):
        cls._instance = None

    def __init__(self, tamanio, n):
        if not hasattr(self, 'initialized'):
            self.idPoblacion = 1 
            self.poblacion = []
            self.tamanio = tamanio
            self.n = n
            self.generarPoblacion(tamanio, n)
            self.initialized = True


    def generarPoblacion(self, tamanio, n):
        for i in range(tamanio):
            random.seed()
            vector = []
            for j in range(int(((n*n)-n)/2)):
                random.seed()
                esInverso = random.choice([True, False])
                if esInverso:
                    vector.append(1 / random.randint(1,9))
                else:
                    vector.append(random.randint(1,10))
            solucionGenerada = Solucion(self.idPoblacion, vector, -1, -1)
            self.poblacion.append(solucionGenerada)
            self.idPoblacion += 1


    def calcularEigenValor(self, vectorRepresentacion):
        matriz = np.eye(self.n)
        cont = 0
        for i in range(self.n):
            for j in range(i+1, self.n):
                matriz[i, j] = vectorRepresentacion[cont]
                cont += 1
                matriz[j, i] = 1 / matriz[i, j]

        eigenvalores = np.linalg.eigvals(matriz)
        eigenvalorMax = np.max(np.abs(eigenvalores))

        return eigenvalorMax, matriz


    def calcularAptitud(self, ALPHA, individuos = None):

        if (individuos is None):
            individuos = self.poblacion

        for individuo in individuos:
            
            eigenvalor, matriz = self.calcularEigenValor(individuo.vectorRepresentacion)

            #aptitud
            limiteSuperiorEigenvalor = self.n + ALPHA * (2.7699 * self.n - 4.3513)
            aptitud = (eigenvalor - self.n) / (limiteSuperiorEigenvalor - self.n)
            
            #Condición para que un individuo sea válido
            esValido = (eigenvalor <= limiteSuperiorEigenvalor)

            #Condición de α para que se cumpla la relación
            esValido = (aptitud <= ALPHA)

            individuo.aptitud, individuo.esValido = aptitud, esValido


    def seleccionarPadres(self, numPadres):
        padres =  []
        disponibles = self.poblacion.copy()
        
        for i in range(numPadres):
            competidores = random.sample(disponibles, 10)
            padreGanador = min(competidores, key=lambda x: x.aptitud)
            padres.append(padreGanador)
            disponibles.remove(padreGanador)

        return padres

    def cruza(self, numPadres):
        hijos = []
        padres = self.seleccionarPadres(numPadres)

        indiceCorte = random.randint(1, len(padres[0].vectorRepresentacion)-1)
        print("Corte: "+str(indiceCorte))

        while (len(padres) != 0):
            padre1Izq = padres[0].vectorRepresentacion[:indiceCorte]
            padre1Der = padres[0].vectorRepresentacion[indiceCorte:]

            padre2Izq = padres[1].vectorRepresentacion[:indiceCorte]
            padre2Der = padres[1].vectorRepresentacion[indiceCorte:]

            vectorHijo1 = padre1Izq
            vectorHijo1.extend(padre2Der)

            vectorHijo2 = padre2Izq
            vectorHijo2.extend(padre1Der)
            
            hijo1 = Solucion(self.idPoblacion, vectorHijo1, -1, -1)
            self.idPoblacion += 1
            hijo2 = Solucion(self.idPoblacion, vectorHijo1, -1, -1)
            self.idPoblacion += 1

            hijos.append(hijo1)
            hijos.append(hijo2)

            padres = padres[2:]
        
        return hijos

    def mutacion(self, hijos, PROBABILIDAD_MUTA):
        for individuo in hijos:
            # Generar índices candidatos según la probabilidad para cada índice del vector
            candidatos = [
                idx for idx in range(len(individuo.vectorRepresentacion))
                if random.random() <= PROBABILIDAD_MUTA
            ]
            
            random.shuffle(candidatos)
            if len(candidatos) % 2 != 0:
                candidatos.pop()
            
            while len(candidatos) > 1:
                i = candidatos.pop(0)
                j = candidatos.pop(0)
                individuo.vectorRepresentacion[i], individuo.vectorRepresentacion[j] = (
                    individuo.vectorRepresentacion[j],
                    individuo.vectorRepresentacion[i],
                )

    def ordenarSegunAptitud(self):
        self.poblacion.sort(key=lambda x: x.aptitud, reverse=False)

    def reemplazarPoblacion(self, hijos):
        self.poblacion = self.poblacion[:len(self.poblacion)-len(hijos)]
        self.poblacion.extend(hijos)

    def ordenarValidos(self):
        soluciones_validas = [individuo for individuo in self.poblacion if individuo.esValido]
        soluciones_validas.sort(key=lambda x: x.aptitud, reverse=True)
        return soluciones_validas