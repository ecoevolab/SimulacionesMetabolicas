import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np

# --- 1. DATA LOADING ---
df1_reacs = pd.read_csv('./04_resultados/rizo/reacciones/conteo_dimont.csv')
df2_reacs = pd.read_csv('./04_resultados/rizo/reacciones/conteo_eggnog.csv')
df3_reacs = pd.read_csv('./04_resultados/rizo/reacciones/conteo_prokka.csv')

# --- 2. FUSIÓN ---

JOIN_KEY = 'Model ID'

# Merge Dimont + EggNOG (df1 + df2)
df_temp = pd.merge(
    df1_reacs,
    df2_reacs,
    on=JOIN_KEY,
    how='inner',
    suffixes=('dimont', 'eggnog')
)

# Merge con Prokka
df_sincronizado = pd.merge(
    df_temp,
    df3_reacs,
    on=JOIN_KEY,
    how='inner'
)

# Renombrar columnas de Prokka para consistencia
df_sincronizado.rename(columns={
    'Total Reactions': 'Total Reactions prokka',
    'Total Metabolites': 'Total Metabolites prokka',
    'Total Genes': 'Total Genes prokka'
}, inplace=True)

print("\nColumnas finales del DataFrame sincronizado:")
print(df_sincronizado.columns)

# --- 3. KRUSKAL-WALLIS ---

grupos_para_kruskal = [
    df_sincronizado['Total Reactions dimont'].values,
    df_sincronizado['Total Reactions eggnog'].values,
    df_sincronizado['Total Reactions prokka'].values
]

H_statistic, p_value = stats.kruskal(*grupos_para_kruskal)

print("\n--- Resultado de la Prueba de Kruskal-Wallis ---")
print("Comparación: Dimont vs EggNOG vs Prokka")
print(f"Estadístico H: {H_statistic:.4f}")
print(f"Valor p: {p_value:.4f}")
print("----------------------------------------")

alpha = 0.05
if p_value < alpha:
    print("✅ Diferencia estadísticamente significativa (p < 0.05)")
else:
    print("❌ No hay diferencia estadísticamente significativa (p > 0.05)")

# --- 4. BOXPLOT ---

nombres_metodos = ['Dimont', 'EggNOG', 'Prokka']

max_valor = np.concatenate(grupos_para_kruskal).max()

plt.figure(figsize=(8, 6))

plt.boxplot(grupos_para_kruskal,
            labels=nombres_metodos,
            patch_artist=True,
            medianprops={'color': 'red', 'linewidth': 2},
            boxprops={'facecolor': 'lightblue', 'edgecolor': 'darkblue'})

plt.text(1.5, max_valor * 1.05,
         f'Kruskal-Wallis H={H_statistic:.2f}\np-value: {p_value:.3e}',
         ha='center', fontsize=10,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

plt.title('Diferencia de Conteo de Reacciones por Método de Anotación')
plt.xlabel('Método de Anotación', fontsize=12)
plt.ylabel('Total de Reacciones', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()



# from scipy.stats import kruskal
# import pandas as pd
# import scipy.stats as stats
# import matplotlib.pyplot as plt

# import os
# # --- 1. DATOS DE EJEMPLO ---
# # Usamos el mismo DataFrame para la consistencia
# data = {
#     'Valor': [20, 22, 25, 23, 27, 
#               15, 18, 17, 19, 16, 
#               30, 32, 35, 31, 34],
#     'Grupo': ['Cepa A', 'Cepa A', 'Cepa A', 'Cepa A', 'Cepa A',
#               'Cepa B', 'Cepa B', 'Cepa B', 'Cepa B', 'Cepa B',
#               'Cepa C', 'Cepa C', 'Cepa C', 'Cepa C', 'Cepa C']
# }
# df = pd.DataFrame(data)

# # --- 2. PREPARACIÓN PARA KRUSKAL-WALLIS Y PLOTEO ---

# # Crea la lista de arrays, uno por cada grupo (necesario para scipy.stats)
# grupos_separados = [df['Valor'][df['Grupo'] == g].values for g in df['Grupo'].unique()]
# nombres_grupos = df['Grupo'].unique()

# # Ejecutar la prueba
# H_statistic, p_value = stats.kruskal(*grupos_separados)

# print("--- Resultado de la Prueba de Kruskal-Wallis ---")
# print(f"Estadístico H: {H_statistic:.4f}")
# print(f"Valor p: {p_value:.4f}")
# print("-" * 40)

# # --- 3. GRÁFICO BOXPLOT CON MATPLOTLIB ---

# plt.figure(figsize=(8, 6))

# # La función boxplot de Matplotlib toma una lista de arrays como entrada
# plt.boxplot(grupos_separados, 
#             labels=nombres_grupos, # Nombres en el eje X
#             patch_artist=True,    # Permite colorear las cajas
#             medianprops={'color': 'red'}, # Estilo para la mediana
#             boxprops={'facecolor': 'lightblue'} # Color de la caja
#            )

# # Opcional: Añadir un título y etiquetas
# plt.title('Comparación de Valores por Grupo (Kruskal-Wallis)')
# plt.xlabel('Grupos (Cepas/Tratamientos)')
# plt.ylabel('Valor de Crecimiento/Metabolito')
# plt.grid(axis='y', linestyle='--', alpha=0.7)

# # Opcional: Añadir el resultado p al gráfico para contexto
# plt.text(0.5, df['Valor'].max() * 1.05, 
#          f'Kruskal-Wallis: p={p_value:.3e}', 
#          ha='center', fontsize=10, 
#          bbox=dict(facecolor='white', alpha=0.5))

# plt.show()

###############################################