import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

df1 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_prokka_carveme_lb.csv')
df2 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_dimont_carveme_lb.csv')

df1_reacs = pd.DataFrame(df1)
df2_reacs = pd.DataFrame(df2)

model_ids = df2_reacs['Model ID']

total_reactions1 = df1_reacs.iloc[1:9, 1]
print(len(total_reactions1))

total_reactions2 = df2_reacs['Total Reactions']
print(len(total_reactions2))

bar_width = 0.35 
r_reactions1 = np.arange(len(model_ids)) # Posiciones para Reacciones
r_reactions2 = [x + bar_width for x in r_reactions1] # Posición DESPLAZADA para Metabolitos


plt.figure(figsize=(12, 6))

# 1. Plotear la primera serie (Reacciones)
plt.bar(r_reactions1, total_reactions1, 
        color='#1F77B4', 
        width=bar_width, 
        label='Total de Reacciones')

# 2. Plotear la segunda serie (Metabolitos)
plt.bar(r_reactions2, total_reactions2, 
        color='#FF7F0E', 
        width=bar_width, 
        label='Total de Metabolitos')


# --- 5. CONFIGURACIÓN FINAL ---

plt.xlabel('Modelo ID', fontsize=12)
plt.ylabel('Conteo', fontsize=12)
plt.title('Comparación Agrupada: Tamaño de la Red Metabólica', fontsize=14)

# Definir las etiquetas del eje X en las posiciones centrales
plt.xticks([r + bar_width / 2 for r in r_reactions1], model_ids, rotation=45, ha='right', fontsize=10)

plt.legend(loc='upper left')
plt.tight_layout()
plt.show()


