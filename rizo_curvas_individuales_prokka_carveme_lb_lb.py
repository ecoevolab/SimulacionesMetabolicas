# ------------------------------------------------------
# Cargar paquetes 
# ------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
# # ---------------------
# Buscar archivos CSV
# ---------------------
csv_files = glob.glob('/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomasa_24horas/resultados/ST*_prokka_carveme_lb_biomasa_24hrs.csv')
# --------------------------
# Asignar colores a los ids
# --------------------------
colores_bac = {
    'ST00000': '#00FF00', 
    'ST00060': '#D4807C', # Arthrobacter
    'ST00094': '#C76662', # Rhodococcus 
    'ST00101': '#5F9EAD', # Pseudomonas
    'ST00110': '#B7464C', # Pseudomonas 
    'ST00164': '#9E3345', # Ballicus thuringesis 
    'ST00143': '#752530', # Paenibacillus
    'ST00042': '#80B6B3', # Pseudomonas umsongensis 
    'ST00109': '#3D788E', # Mycobacterium
    'ST00154': '#26526B', # Agrobacterium
    'ST00046': '#1A3749'  # Bacillus
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
    'ST00164': r'$\it{Ballicus thuringesis\ sp.}$', 
    'ST00143': r'$\it{Paenibacillus\ sp.}$',
    'ST00042': r'$\it{Pseudomonas\ umsongensis}$', 
    'ST00109': r'$\it{Mycobacterium\ sp.}$', 
    'ST00154': r'$\it{Agrobacterium\ sp.}$', 
    'ST00046': r'$\it{Bacillus\ sp.}$' 
}

for file in csv_files:
    file_name = os.path.basename(file)
    model_id = file_name.replace('_prokka_carveme_lb_biomasa_24hrs.csv', '')
    scientific_name = name_bac.get(model_id)
    final_label = f"{scientific_name} ({model_id})"
    cepa_color = colores_bac.get(model_id, 'black')
    try:
        df = pd.read_csv(file)
        tiempo = df.iloc[:, 0]
        masa = df.iloc[:, 1]
        plt.figure(figsize=(20, 8))
        plt.plot(tiempo, masa, 
        marker='o', 
        linestyle='-', 
        color= cepa_color,
        label= final_label)
        plt.title(f"Curvas de Crecimiento Microbiano para {scientific_name}")
        #plt.xlabel('Tiempo (Ciclos de Simulación)')
        plt.xlabel('Tiempo (Ciclos de Simulación)')
        plt.ylabel('Biomasa [ln(g)]')
        plt.grid(True, linestyle='--', alpha=0.6)
        output_folder = '04_resultados/rizo/graficas'
        output_path = os.path.join(output_folder, f"{model_id}_prokka_carveme_lb_biomasa_24hrs.png")
        plt.savefig(output_path)
        plt.show()

        plt.legend(title='Modelo ID', bbox_to_anchor=(1.05, 1), loc='upper left') 
    except Exception as e:
        print(f"Error al cargar {file_name}: {e}")

plt.show()