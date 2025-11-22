from scipy.stats import kruskal
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

import os
# # --- 1. DATOS DE EJEMPLO ---
# # Usamos el mismo DataFrame para la consistencia
data = {
     'Valor': [20, 22, 25, 23, 27, 
               15, 18, 17, 19, 16, 
               30, 32, 35, 31, 34],
     'Grupo': ['Cepa A', 'Cepa A', 'Cepa A', 'Cepa A', 'Cepa A',
               'Cepa B', 'Cepa B', 'Cepa B', 'Cepa B', 'Cepa B',
               'Cepa C', 'Cepa C', 'Cepa C', 'Cepa C', 'Cepa C']
 }
df = pd.DataFrame(data)

# # --- 2. PREPARACIÓN PARA KRUSKAL-WALLIS Y PLOTEO ---

# # Crea la lista de arrays, uno por cada grupo (necesario para scipy.stats)
grupos_separados = [df['Valor'][df['Grupo'] == g].values for g in df['Grupo'].unique()]
nombres_grupos = df['Grupo'].unique()

# # Ejecutar la prueba
H_statistic, p_value = stats.kruskal(*grupos_separados)

print("--- Resultado de la Prueba de Kruskal-Wallis ---")
print(f"Estadístico H: {H_statistic:.4f}")
print(f"Valor p: {p_value:.4f}")
print("-" * 40)

# # --- 3. GRÁFICO BOXPLOT CON MATPLOTLIB ---

plt.figure(figsize=(8, 6))

# # La función boxplot de Matplotlib toma una lista de arrays como entrada
plt.boxplot(grupos_separados, 
             labels=nombres_grupos, # Nombres en el eje X
             patch_artist=True,    # Permite colorear las cajas
             medianprops={'color': 'red'}, # Estilo para la mediana
             boxprops={'facecolor': 'lightblue'} # Color de la caja
            )

# # Opcional: Añadir un título y etiquetas
plt.title('Comparación de Valores por Grupo (Kruskal-Wallis)')
plt.xlabel('Grupos (Cepas/Tratamientos)')
plt.ylabel('Valor de Crecimiento/Metabolito')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# # Opcional: Añadir el resultado p al gráfico para contexto
plt.text(0.5, df['Valor'].max() * 1.05, 
          f'Kruskal-Wallis: p={p_value:.3e}', 
          ha='center', fontsize=10, 
          bbox=dict(facecolor='white', alpha=0.5))

plt.show()
