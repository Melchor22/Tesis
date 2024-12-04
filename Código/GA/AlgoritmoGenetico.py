import random
import numpy as np
from deap import base, creator, tools, algorithms

class EigenvalueProblem:
    def __init__(self, n, alpha):
        self.n = n
        self.alpha = alpha

    def calcularEigenValor(self, vectorRepresentacion):
        matriz = np.eye(self.n)
        cont = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                matriz[i, j] = vectorRepresentacion[cont]
                cont += 1
                matriz[j, i] = 1 / matriz[i, j]

        eigenvalores = np.linalg.eigvals(matriz)
        eigenvalorMax = np.max(np.abs(eigenvalores))
        return eigenvalorMax, matriz

    def calcularAptitud(self, vectorRepresentacion):
        eigenvalor, matriz = self.calcularEigenValor(vectorRepresentacion)

        # Calcular el límite superior del eigenvalor
        limiteSuperiorEigenvalor = self.n + self.alpha * (2.7699 * self.n - 4.3513)
        aptitud = (eigenvalor - self.n) / (limiteSuperiorEigenvalor - self.n)

        # Verificar validez
        esValido = (eigenvalor <= limiteSuperiorEigenvalor) and (eigenvalor <= self.alpha)
        return aptitud, esValido

# Configuración del problema
n = 4  # Tamaño de la matriz
alpha = 1.5
eigenvalue_problem = EigenvalueProblem(n, alpha)

# Configuración del algoritmo genético
def evalFitness(individual):
    vector = list(individual)
    aptitud, esValido = eigenvalue_problem.calcularAptitud(vector)
    # Penalizar individuos no válidos
    return (aptitud if esValido else float("inf"),)

def main():
    # Crear tipos de datos
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar aptitud
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # Definir atributos: un número real entre 0.1 y 10.0
    toolbox.register("attr_float", random.uniform, 0.1, 10.0)

    # Crear un individuo: un vector de representación para la matriz
    num_variables = int((n * (n - 1)) / 2)  # Número de elementos únicos del vector
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=num_variables)

    # Crear una población: lista de individuos
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Operadores genéticos
    toolbox.register("evaluate", evalFitness)  # Evaluación de aptitud
    toolbox.register("mate", tools.cxOnePoint)  # Cruce de un punto integrado
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.0, indpb=0.2)  # Mutación Gaussiana
    toolbox.register("select", tools.selTournament, tournsize=2)  # Selección por torneo

    # Inicializar población
    population = toolbox.population(n=100)

    # Estadísticas para seguimiento
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fitnesses: sum(fitnesses) / len(fitnesses))
    stats.register("min", min)
    stats.register("max", max)

    # Ejecutar el algoritmo genético
    population, logbook = algorithms.eaSimple(
        population,
        toolbox,
        cxpb=0.7,  # Probabilidad de cruce
        mutpb=0.2,  # Probabilidad de mutación
        ngen=50,  # Número de generaciones
        stats=stats,
        verbose=True
    )

    # Mejor individuo encontrado
    best_ind = tools.selBest(population, k=1)[0]
    print("Mejor individuo (vector):", best_ind)
    print("Aptitud del mejor individuo:", best_ind.fitness.values[0])

if __name__ == "__main__":
    main()
