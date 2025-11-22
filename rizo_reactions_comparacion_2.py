import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. CARGA DE DATOS ---
df1_reacs = pd.read_csv('04_resultados/rizo/reacciones/reacciones_totales_reactions_dimont_carveme_lb_4.csv')
df2_reacs = pd.read_csv('04_resultados/rizo/reacciones/reacciones_totales_reactions_prokka_carveme_lb_4.csv')
df3_reacs = pd.read_csv('04_resultados/rizo/reacciones/reacciones_totales_eggnog_carveme.csv')

# --- 2. FUSIÓN CRÍTICA (Fusión Secuencial y Sincronización) ---

# Paso A: Fusionar Dimont (df1) y Prokka (df2)
df_temp = pd.merge(
    df1_reacs, 
    df2_reacs, 
    on='Model_ID', # NOTA: Se corrige a 'Model ID' (con espacio)
    how='inner', 
    suffixes=('_dimont', '_prokka') 
)

# Paso B: Fusionar el resultado con Eggnote (df3). La columna de Eggnote no necesita sufijo si es única.
df_sincronizado = pd.merge(
    df_temp, 
    df3_reacs, 
    on='Model_ID', 
    how='inner' 
)

# # --- 3. EXTRACCIÓN DE DATOS SINCRONIZADOS ---

N = len(df_sincronizado) # Longitud final sincronizada
model_ids = df_sincronizado['Model_ID'] # Etiquetas X

# Extracción de Datos Y (Usando los sufijos generados y el nombre de columna original)
total_reactions1 = df_sincronizado['Total_Reactions_dimont'] # Dimont
total_reactions2 = df_sincronizado['Total_Reactions_prokka'] # Prokka
total_reactions3 = df_sincronizado['Total_Reactions']        # Eggnote (No tiene sufijo)

# # --- 4. CÁLCULO DE POSICIONES (3 Series) ---
bar_width = 0.30 
r1 = np.arange(N) 
r2 = [x + bar_width for x in r1] 
r3 = [x + bar_width for x in r2]


plt.figure(figsize=(14, 7))

# # 1. Plotear Dimont
plt.bar(r1, total_reactions1, 
         color='#1F77B4', 
         width=bar_width, 
         label='Dimont Annotation')

# # 2. Plotear Prokka
plt.bar(r2, total_reactions2, 
         color='#FF7F0E', 
         width=bar_width, 
         label='Prokka Annotation',
         hatch='//') 

# # 3. Plotear Eggnote
plt.bar(r3, total_reactions3, 
         color='#2CA02C', 
         width=bar_width, 
         label='EggNOG Annotation')


# # --- 5. CONFIGURACIÓN FINAL ---
plt.xlabel('Strain ID', fontsize=12)
plt.ylabel('Number of Reactions', fontsize=12)
plt.title('Comparison of Metabolic Network Size by Annotation Approach', fontsize=14)

# # Definir las etiquetas del eje X centradas en las 3 barras
plt.xticks([r + bar_width for r in r1], model_ids, rotation=45, ha='right', fontsize=10)

plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
plt.tight_layout()
plt.show()