import random
import cupy as cp  # Reemplaza numpy con cupy
from solucion import Solucion

class AlgoritmoGenetico:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AlgoritmoGenetico, cls).__new__(cls)
        return cls._instance

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
            vector = cp.array([1 / random.randint(1,9) if random.choice([True, False]) else random.randint(1,10)
                               for _ in range(int(((n*n)-n)/2))])
            solucionGenerada = Solucion(self.idPoblacion, vector, -1, -1)
            self.poblacion.append(solucionGenerada)
            self.idPoblacion += 1

    def calcularEigenValor(self, vectorRepresentacion):
        matriz = cp.eye(self.n)
        cont = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                matriz[i, j] = vectorRepresentacion[cont]
                matriz[j, i] = 1 / matriz[i, j]
                cont += 1
        eigenvalores = cp.linalg.eigvals(matriz)
        eigenvalorMax = cp.max(cp.abs(eigenvalores))
        return eigenvalorMax, matriz

    def calcularAptitud(self, ALPHA, individuos=None):
        if individuos is None:
            individuos = self.poblacion
        for individuo in individuos:
            eigenvalor, _ = self.calcularEigenValor(individuo.vectorRepresentacion)
            limiteSuperiorEigenvalor = self.n + ALPHA * (2.7699 * self.n - 4.3513)
            aptitud = (eigenvalor - self.n) / (limiteSuperiorEigenvalor - self.n)
            esValido = (eigenvalor <= limiteSuperiorEigenvalor)
            individuo.aptitud, individuo.esValido = aptitud, esValido

    def ordenarSegunAptitud(self):
        self.poblacion.sort(key=lambda x: x.aptitud, reverse=False)

    def reemplazarPoblacion(self, hijos):
        # Mantén la población en la GPU asegurándote de que las referencias sean correctas
        self.poblacion = self.poblacion[:len(self.poblacion) - len(hijos)]
        self.poblacion.extend(hijos)

    def ordenarValidos(self):
        # Filtra individuos válidos en la GPU
        soluciones_validas = [individuo for individuo in self.poblacion if individuo.esValido]
        # Ordena en la GPU según la aptitud, en orden descendente
        soluciones_validas.sort(key=lambda x: x.aptitud, reverse=True)
        return soluciones_validas