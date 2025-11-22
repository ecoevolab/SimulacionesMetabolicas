import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# -----------------------------------
# Definición de Variables y Paletas
# -----------------------------------

# Nota: Asumimos que tus DataFrames df1_reacs y df2_reacs tienen el mismo orden y longitud.

colores_bac = {
    'ST00000': '#00FF00', 'ST00060': '#D4807C', 'ST00094': '#C76662', 
    'ST00101': '#5F9EAD', 'ST00110': '#B7464C', 'ST00164': '#9E3345',
    'ST00143': '#752530', 'ST00042': '#80B6B3', 'ST00109': '#3D788E', 
    'ST00154': '#26526B', 'ST00046': '#1A3749'
}

# --- Carga y Extracción de Datos (Asumido Correcto) ---
df1_reacs = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_dimont_carveme_lb_4.csv')
df2_reacs = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_prokka_carveme_lb_4.csv')

model_ids = df1_reacs['Model ID']
total_reactions1 = df1_reacs['Total Reactions']
total_reactions2 = df2_reacs['Total Reactions']
N = len(model_ids) # Longitud de los datos

bar_width = 0.35 
r_reactions1 = np.arange(N)
r_reactions2 = [x + bar_width for x in r_reactions1] 

# --- PASO CRÍTICO: GENERAR LA LISTA DE COLORES ORDENADA ---

# Itera sobre los IDs del DataFrame y busca el color en el diccionario.
bar_color_sequence = [colores_bac.get(model_id, 'gray') for model_id in model_ids]

# -------------------------------------------------------------------------
# PLOTEO Y CONFIGURACIÓN
# -------------------------------------------------------------------------

plt.figure(figsize=(10, 6))

# 1. Plotear la primera serie (Dimont)
plt.bar(r_reactions1, total_reactions1, 
        color=bar_color_sequence, # <--- CORRECCIÓN: Usa la lista de N colores
        edgecolor='black',
        linewidth=1.5,
        width=bar_width,
        hatch='/')
        #label='Dimont Annotation')


# 2. Plotear la segunda serie (Prokka)
plt.bar(r_reactions2, total_reactions2, 
        color=bar_color_sequence, # <--- Aplica la misma secuencia de colores
        width=bar_width, 
        edgecolor='black',
        linewidth=1.5)
        #label='Prokka Annotation')


# --- CONFIGURACIÓN FINAL ---

plt.xlabel('Strain ID', fontsize=12)
plt.ylabel('Number of Reactions', fontsize=12)
plt.title('Comparison of Metabolic Network Size by Annotator', fontsize=14)

# Definir las etiquetas del eje X
plt.xticks([r + bar_width / 2 for r in r_reactions1], model_ids, rotation=45, ha='right', fontsize=10)

# 3. CAMBIAR EL COLOR DE LA LEYENDA A NEGRO (Si se desea)
legend = plt.legend(loc='upper left', frameon=False) 
for text in legend.get_texts():
    text.set_color('black')

plt.tight_layout()
plt.show()