# ----------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np 
import os 
import matplotlib.cm as cm 
import math
# ------------------------------------
# Crear variables
# ------------------------------------
# Encontrar todos los archivos CSV de biomasa
csv_files = glob.glob('/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomasa_24horas/resultados/ST*_prokka_carveme_lb_biomasa_24hrs.csv')
# Diccionario para almacenar los DataFrames cargados
ALL_GROWTH_DATA = {} 
colores_bac = {
    'ST00000': '#00FF00', 
    'ST00060': '#D4807C', # Arthrobacter
    'ST00094': '#C76662', # Rhodococcus 
    'ST00101': '#5F9EAD', # Pseudomonas
    'ST00110': '#B7464C', # Pseudomonas 
    'ST00164': '#9E3345', # Ballicus thuringesis #🤔
    'ST00143': '#752530', # Paenibacillus
    'ST00042': '#80B6B3', # Pseudomonas umsongensis #🤔
    'ST00109': '#3D788E', # Mycobacterium
    'ST00154': '#26526B', # Agrobacterium
    'ST00046': '#1A3749'  # Bacillus (Usando el color más oscuro de la escala azul)
}
name_bac = { 
    'ST00000': r'$\it{Escherichia\ sp.}$',
    'ST00060': r'$\it{Arthrobacter\ sp.}$', 
    'ST00094': r'$\it{Rhodococcus\ erythropolis}$', 
    'ST00101': r'$\it{Pseudomonas\ sp.}$', 
    'ST00110': r'$\it{Variovorax\ paradoxus}$', 
    'ST00164': r'$\it{Ballicus thuringesis\ sp.}$', 
    'ST00143': r'$\it{Paenibacillus\ sp.}$', 
    'ST00042': r'$\it{Pseudomonas umsongensis\ sp.}$', 
    'ST00109': r'$\it{Mycobacterium\ sp.}$', 
    'ST00154': r'$\it{Agrobacterium\ sp.}$', 
    'ST00046': r'$\it{Bacillus\ sp.}$' 
}

print(f"Archivos CSV encontrados: {len(csv_files)}")
# ----------------------------------------------------
# Ciclo para cargar todos los datos 
# ------------------------------------------------
for file_path in csv_files:    
    try:
        df = pd.read_csv(file_path)
        
        # Extraer el ID del modelo 
        file_name = os.path.basename(file_path)
        model_id = file_name.replace('_prokka_carveme_lb_biomasa_24hrs.csv', '') 

        scientific_name = name_bac.get(model_id)
        final_label = f"{scientific_name} ({model_id})"
        
        # Almacenar el DataFrame
        ALL_GROWTH_DATA[model_id] = df
        
    except Exception as e:
        print(f"Error al cargar {file_name}: {e}")

# -------------------------------------
# Graficar 
# -------------------------------------
plt.figure(figsize=(12, 12))

# Seleccionar eje x, tiempo 
primer_df = list(ALL_GROWTH_DATA.values())[0] 
NUM_ROWS = len(primer_df)

time_step = 0.1 
cycles = np.arange(NUM_ROWS) 

#Modificar de ciclos a horas
tiempo = cycles * time_step 

# Graficar cada modelo
for model_id, df in ALL_GROWTH_DATA.items():
    # Extraer la biomasa (eje Y) 
    masa = df.iloc[:, 1]
    log_masa = np.log10(masa + 1e-10) # Log-transformado para el crecimiento
    cepa_color = colores_bac.get(model_id, 'gray')

    plt.plot(tiempo, log_masa, 
             linestyle='-', 
             linewidth=8,
             color= cepa_color, 
             label=model_id) 
    


plt.xlabel('time (h)', fontsize=20)



plt.ylabel(r'biomass [$\it{log10}$($\bf{g}$)]', fontsize=20)#texto_descriptivo = "Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe \ny Gapfilling con medio LB."


plt.grid(True, linestyle='--', alpha=0.5)

plt.legend(title='Strain ID', bbox_to_anchor=(1.05, 1), loc='upper center') 
output_folder = '04_resultados/rizo/graficas'
output_path = os.path.join(output_folder, "comparacion_curvas_prokka_carveme_lb_biomasa_24cd hrs.png")
plt.savefig(output_path)


plt.show()
