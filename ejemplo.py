import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. CARGAR DATOS (Asumiendo que has generado dos archivos CSV) ---

# Sustituye estas rutas por las rutas reales de tus CSV consolidados
REACTIONS_PATH = os.path.join('04_resultados', 'conteo_reacciones_final.csv')
METABOLITES_PATH = os.path.join('04_resultados', 'conteo_metabolitos_final.csv')

# Suponemos que los DataFrames son:
# df_reactions: | Model ID | Total Reactions |
# df_metabolites: | Model ID | Total Metabolites |

# --- NOTA: Usaré datos de ejemplo para que el código sea funcional ---
data_rxn = {
    'Model ID': ['ST00046', 'ST00109', 'ST00143'],
    'Total Reactions': [1020, 955, 1150]
}
data_met = {
    'Model ID': ['ST00046', 'ST00109', 'ST00143'],
    'Total Metabolites': [980, 890, 1070]
}
df_reactions = pd.DataFrame(data_rxn)
df_metabolites = pd.DataFrame(data_met)
# --------------------------------------------------------------------


# --- 2. PREPARACIÓN DE POSICIÓN Y EXTRACCIÓN DE DATOS ---

# Eje X: Los IDs de los modelos (Mismo en ambos DFs)
model_ids = df_reactions['Model ID']

# Series de Datos (Eje Y)
total_reactions = df_reactions['Total Reactions']
total_metabolites = df_metabolites['Total Metabolites'] # Extraído del SEGUNDO DataFrame


# 3. Preparar el offset para agrupar las barras
bar_width = 0.35 
r_reactions = np.arange(len(model_ids)) # Posiciones para Reacciones
r_metabolites = [x + bar_width for x in r_reactions] # Posición DESPLAZADA para Metabolitos


# --- 4. PLOTEO DE BARRAS AGRUPADAS ---

plt.figure(figsize=(12, 6))

# 1. Plotear la primera serie (Reacciones)
plt.bar(r_reactions, total_reactions, 
        color='#1F77B4', 
        width=bar_width, 
        label='Total de Reacciones')

# 2. Plotear la segunda serie (Metabolitos)
plt.bar(r_metabolites, total_metabolites, 
        color='#FF7F0E', 
        width=bar_width, 
        label='Total de Metabolitos')


# --- 5. CONFIGURACIÓN FINAL ---

plt.xlabel('Modelo ID', fontsize=12)
plt.ylabel('Conteo', fontsize=12)
plt.title('Comparación Agrupada: Tamaño de la Red Metabólica', fontsize=14)

# Definir las etiquetas del eje X en las posiciones centrales
plt.xticks([r + bar_width / 2 for r in r_reactions], model_ids, rotation=45, ha='right', fontsize=10)

plt.legend(loc='upper left')
plt.tight_layout()
plt.show()