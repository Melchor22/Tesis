import pandas as pd
import matplotlib.pyplot as plt

class GraficoConvergencia:
    def __init__(self, archivo_csv):
        # Cargar los datos del archivo CSV
        self.data = pd.read_csv(archivo_csv)
        print("Columnas detectadas en el CSV:", self.data.columns)

    def obtener_ejecuciones_ordenadas(self):
        # Obtener el último valor de "Mejor Aptitud" para cada ejecución
        ultimas_aptitudes = self.data.groupby("Ejecucion")["Mejor Aptitud"].last()
        # Ordenar las ejecuciones por el último valor (de menor a mayor)
        ejecuciones_ordenadas = ultimas_aptitudes.sort_values().index.tolist()
        return ejecuciones_ordenadas

    def generar_graficas(self, nombre_salida="convergencia.png"):
        # Obtener las ejecuciones ordenadas
        ejecuciones_ordenadas = self.obtener_ejecuciones_ordenadas()

        # Seleccionar peor, mejor e intermedia ejecución
        peor_ejecucion = ejecuciones_ordenadas[-1]  # Última ejecución (mayor valor)
        mejor_ejecucion = ejecuciones_ordenadas[0]  # Primera ejecución (menor valor)
        ejecucion_intermedia = ejecuciones_ordenadas[len(ejecuciones_ordenadas) // 2]

        # Filtrar datos correspondientes
        datos_peor = self.data[self.data["Ejecucion"] == peor_ejecucion]
        datos_mejor = self.data[self.data["Ejecucion"] == mejor_ejecucion]
        datos_intermedia = self.data[self.data["Ejecucion"] == ejecucion_intermedia]

        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(
            datos_peor["Generacion"],
            datos_peor["Mejor Aptitud"],
            label=f"Peor Ejecución ({peor_ejecucion})",
            linestyle='--', color='red'
        )
        plt.plot(
            datos_intermedia["Generacion"],
            datos_intermedia["Mejor Aptitud"],
            label=f"Ejecución Intermedia ({ejecucion_intermedia})",
            linestyle='-.', color='blue'
        )
        plt.plot(
            datos_mejor["Generacion"],
            datos_mejor["Mejor Aptitud"],
            label=f"Mejor Ejecución ({mejor_ejecucion})",
            linestyle='-', color='green'
        )

        # Configurar el gráfico
        plt.title("Gráfica de Convergencia")
        plt.xlabel("Generación")
        plt.ylabel("Mejor Aptitud")
        plt.legend()
        plt.grid(True)
        plt.savefig(nombre_salida)
        plt.show()

# Uso
graficas = GraficoConvergencia("ejecuciones.csv")
graficas.generar_graficas("graficas_convergencia_mejorada.png")