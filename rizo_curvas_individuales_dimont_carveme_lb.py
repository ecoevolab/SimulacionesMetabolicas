# ------------------------------------------------------
# Cargar paquetes 
# ------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
# ---------------------
# Buscar archivos CSV
# ---------------------
csv_files = glob.glob('./04_resultados/rizo/biomasas/*_dimont_carveme_lb_1_este.csv')

# --------------------------
# Asignar colores a los ids
# --------------------------
colores_bac = {
    'ST00000': '#00FF00', 
    'ST00060': '#D4807C',
    'ST00094': '#C76662',
    'ST00101': '#5F9EAD',
    'ST00110': '#B7464C',
    'ST00164': '#9E3345',  # Bacillus thuringiensis ✅
    'ST00143': '#752530',
    'ST00109': '#3D788E',
    'ST00154': '#26526B',
    'ST00046': '#1A3749'
}

# ---------------------------------------
# Asignar nombres científicos a los ids
# --------------------------------------
name_bac = { 
    'ST00000': r'$\it{Escherichia\ sp.}$',
    'ST00060': r'$\it{Arthrobacter\ sp.}$',
    'ST00094': r'$\it{Rhodococcus\ erythropolis}$',
    'ST00101': r'$\it{Pseudomonas\ sp.}$',
    'ST00110': r'$\it{Variovorax\ paradoxus}$',
    'ST00164': r'$\it{Bacillus\ thuringiensis}$', 
    'ST00143': r'$\it{Paenibacillus\ sp.}$',
    'ST00109': r'$\it{Mycobacterium\ sp.}$',
    'ST00154': r'$\it{Agrobacterium\ sp.}$',
    'ST00046': r'$\it{Bacillus\ sp.}$'
}

# --------------------------------------
# Crear carpeta de salida si no existe
# --------------------------------------
output_folder = '04_resultados/rizo/graficas'
os.makedirs(output_folder, exist_ok=True)

for file in csv_files:
    file_name = os.path.basename(file)
    model_id = file_name.replace('_dimont_carveme_lb_1_este.csv', '')

    scientific_name = name_bac.get(model_id, 'Nombre desconocido')
    final_label = f"{scientific_name} ({model_id})"
    cepa_color = colores_bac.get(model_id, 'black')

    try:
        df = pd.read_csv(file)
        tiempo = (df.iloc[:, 0]*0.1)
        masa = df.iloc[:, 1]
        log_masa = np.log10(masa + 1e-10) # Log-transformado para el crecimiento


        plt.figure(figsize=(20, 8))
        plt.plot(
            tiempo, log_masa,
            marker='o',
            linestyle='-',
            color=cepa_color,
            label=final_label
        )

        plt.title(f"Curva de Crecimiento para {scientific_name}")
        plt.xlabel(
            't(h)'
        )
        plt.ylabel(r'Biomasa [$\it{log10}$($\bf{g}$)]')
        plt.grid(True, linestyle='--', alpha=0.6)

        # Leyenda ANTES de guardar
        #plt.legend(title='Modelo ID', bbox_to_anchor=(1.05, 1), loc='upper left')

        output_path = os.path.join(output_folder, f"{model_id}_growth_curve_este.png")
        plt.savefig(output_path, bbox_inches='tight')
        plt.show()

    except Exception as e:
        print(f"Error al cargar {file_name}: {e}")
