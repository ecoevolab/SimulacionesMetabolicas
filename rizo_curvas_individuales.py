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

biomas_prokka = glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_treat.csv')
biomas_dimont = glob.glob('./04_resultados/rizo/biomasas/ST*_dimont_carveme_lb_treat.csv')
biomas_eggnog = glob.glob('./04_resultados/rizo/biomasas/ST*_eggnog_carveme_lb_treat.csv')

# ----------------------

biomas_08 = glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_08hrs.csv')
biomas_16 = glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_16hrs.csv')
biomas_24 = glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_24hrs.csv')
biomas_48 = glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_48hrs.csv')

# -------------------------
model_paths = [biomas_prokka, biomas_dimont, biomas_eggnog, biomas_08, biomas_16, biomas_24, biomas_48]

output_folder = '04_resultados/rizo/graficas_2'
os.makedirs(output_folder, exist_ok=True)

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

for grupo in model_paths:
    for individual_model in grupo:
        file_name = os.path.basename(individual_model)
        model_id = file_name[:7]
        if '_prokka_carveme_lb_treat' in file_name:
            treat = '_prokka_carveme_treat'
        elif '_dimont_carveme_lb_treat' in file_name:
            treat = '_dimont_carveme_treat'
        elif '_eggnog_carveme_lb_treat' in file_name:
            treat = '_eggnog_carveme_treat'
        elif '_prokka_carveme_lb_biomasa_08hrs' in file_name:
            treat = '_prokka_carveme_lb_biomasa_08hrs'
        elif '_prokka_carveme_lb_biomasa_16hrs' in file_name:
            treat = '_prokka_carveme_lb_biomasa_16hrs'
        elif '_prokka_carveme_lb_biomasa_24hrs' in file_name:
            treat = '_prokka_carveme_lb_biomasa_24hrs'
        elif '_prokka_carveme_lb_biomasa_48hrs' in file_name:
            treat = '_prokka_carveme_lb_biomasa_48hrs'
        else: 
            treat = 'desconocido'

        scientific_name = name_bac.get(model_id, 'desconocido')
        final_label = f"{model_id}{treat}"
        cepa_color = colores_bac.get(model_id, 'black')
        try:
            df = pd.read_csv(individual_model)
            tiempo = (df.iloc[:, 0]*0.1)
            masa = df.iloc[:, 1]
            log_masa = np.log10(masa + 1e-10)
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
            plt.legend(title='Modelo ID', bbox_to_anchor=(1.05, 1), loc='upper left') 
            output_path = os.path.join(output_folder, f"{final_label}.png")
            plt.savefig(output_path)

        except Exception as e:
            print(f"Error al cargar {file_name}: {e}")

