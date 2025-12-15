import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# -----------------------------------
csv_files = glob.glob('./04_resultados/rizo/biomasas/suma*_prokka_carveme_lb_biomasa_8hrs.csv')

output_folder = './04_resultados/rizo/graficas'
os.makedirs(output_folder, exist_ok=True)

for file in csv_files:
    file_name = os.path.basename(file)
    model_id = file_name.replace('_prokka_carveme_lb_biomasa_8hrs.csv', '')

    try:
        df = pd.read_csv(file)

        # Columnas
        tiempo = df.iloc[:, 0]
        biomasa_1 = df.iloc[:, 1]
        biomasa_2 = df.iloc[:, 2]

        plt.figure(figsize=(20, 8))

        plt.plot(tiempo, biomasa_1, marker='o', linestyle='-', label='Biomasa 1')
        plt.plot(tiempo, biomasa_2, marker='s', linestyle='--', label='Biomasa 2')

        plt.title(f"Curvas de Crecimiento — {model_id}")
        plt.xlabel('Tiempo (Ciclos de Simulación)')
        plt.ylabel('Biomasa')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()

        output_path = os.path.join(
            output_folder, f"{model_id}_biomasa_8hrs.png"
        )

        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"✔ Gráfica generada: {output_path}")

    except Exception as e:
        print(f"✖ Error al procesar {file_name}: {e}")
