import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

csv_files = glob.glob('./04_resultados/rizo/biomasas/comunidad_*.csv')

colores_bac = {
    # Rojo/Marrón (Top 5 del póster)
    'ST00000': '#00FF00', 
    'ST00060': '#D4807C', # Arthrobacter
    'ST00094': '#C76662', # Rhodococcus 
    'ST00101': '#5F9EAD', # Pseudomonas
    'ST00110': '#B7464C', # Pseudomonas 
    'ST00164': '#9E3345', # Bacillus thuringiensis
    'ST00143': '#752530', # Paenibacillus
    # Azul/Cian (Bottom 5 del póster)
    'ST00042': '#80B6B3', # Pseudomonas umsongensis
    'ST00109': '#3D788E', # Mycobacterium
    'ST00154': '#26526B', # Agrobacterium
    'ST00046': '#1A3749'  # Bacillus (azul oscuro)
}

name_bac = { 
    'ST00000': r'$\it{Escherichia\ sp.}$', #✅
    'ST00060': r'$\it{Arthrobacter\ sp.}$', #✅
    'ST00094': r'$\it{Rhodococcus\ erythropolis}$', #✅
    'ST00101': r'$\it{Pseudomonas\ sp.}$', #✅
    'ST00110': r'$\it{Variovorax\ paradoxus}$', #✅
    'ST00164': r'$\it{Ballicus\ thuringesis}$', 
    'ST00143': r'$\it{Paenibacillus\ sp.}$', #✅
    'ST00042': r'$\it{Pseudomonas\ umsongensis}$', #✅
    'ST00109': r'$\it{Mycobacterium\ sp.}$', #✅
    'ST00154': r'$\it{Agrobacterium\ sp.}$', #✅
    'ST00046': r'$\it{Bacillus\ sp.}$' #✅
}



for file in csv_files:
    try:
        df = pd.read_csv(file)

        model_id = os.path.basename(file).replace(".csv", "")

        tiempo = df.iloc[:, 0]   
        tiempo_h = (df.iloc[:, 0]*0.1)

        masa = df.iloc[:, 1:6]   

        log_masa = np.log10(masa + 1e-10)

        plt.figure(figsize=(20, 8))

        for col in log_masa.columns:
            color_asignado = colores_bac.get(col, None)
            nombre_asignaodo = name_bac.get(col, None)

            plt.plot(
                tiempo_h,
                log_masa[col],
                marker='o',
                linestyle='-',
                label=nombre_asignaodo,
                color=color_asignado   
            )

        plt.title(f"Curvas de Crecimiento Microbiano de la {model_id}")
        plt.xlabel("Tiempo (h)")
        plt.ylabel("Biomasa [log10(g)]")
        plt.grid(True, linestyle='--', alpha=0.6)

        plt.legend(title="Strain ID")

        output_folder = '04_resultados/rizo/graficas'
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"{model_id}.png")
        plt.savefig(output_path)

        plt.show()

    except Exception as e:
        print(f"Error al procesar {file}: {e}")
