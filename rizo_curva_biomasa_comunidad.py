import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

csv_files = glob.glob('./04_resultados/rizo/biomasas/*_biomasa_suma.csv')
output_folder = './04_resultados/rizo/'

for file in csv_files:
    comu_name = os.path.basename(file)
    comu_id = comu_name.replace('_biomasa_suma.csv', '')

    try:
        df = pd.read_csv(file)

        # Tiempo (primera columna * 0.1)
        tiempo = df.iloc[:, 0] * 0.1

        # Última columna
        masa = df.iloc[:, -1]

        # Transformado log10 seguro
        log_masa = np.log10(masa + 1e-10)

        # Gráfica
        plt.figure(figsize=(20, 8))
        plt.plot(tiempo, masa, linestyle='-', color='pink')

        plt.title(f"Curva de Crecimiento total | {comu_id}")
        plt.xlabel('t (h)')
        plt.ylabel(r'Biomasa [$\log_{10}$(g)]')
        plt.grid(True, linestyle='--', alpha=0.6)

        # Guardar con nombre único
        output_path = os.path.join(output_folder, f"suma_biomasa_{comu_id}.png")
        plt.savefig(output_path, bbox_inches='tight')

        plt.show()

    except Exception as e:
        print(f"Error al procesar {comu_name}: {e}")
