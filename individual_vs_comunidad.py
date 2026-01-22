import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import os 

# ---------------------------------------------------------
# 1. Configuración de rutas
# ---------------------------------------------------------
archivo_unificado = './04_resultados/rizo/biomasas/unificado_biomasas_08.csv'
archivo_comunidad = './04_resultados/rizo/biomasas/comunidad_1.csv'
output_path = './04_resultados'

# ---------------------------------------------------------
# 2. Carga y preparación de datos
# ---------------------------------------------------------
df_uni = pd.read_csv(archivo_unificado)
df_com = pd.read_csv(archivo_comunidad)

tiempo_uni = df_uni.iloc[:, 0] * 0.1
tiempo_com = df_com.iloc[:, 0] * 0.1

# Encontrar bacterias comunes entre ambos archivos
cols_uni = set(df_uni.columns[1:])
cols_com = set(df_com.columns[1:])
bacterias_comunes = sorted(list(cols_uni & cols_com))

# Paleta de colores para distinguir las 5 bacterias
colores = ['#26526B', '#B7464C', '#5F9EAD', '#752530', '#1A3749']

# ---------------------------------------------------------
# 3. Generar la Gráfica Única
# ---------------------------------------------------------
plt.figure(figsize=(12, 8))

for i, bacteria in enumerate(bacterias_comunes):
    color_actual = colores[i % len(colores)]
    
    # Graficar datos del Unificado (Línea Continua)
    plt.plot(tiempo_uni, np.log10(df_uni[bacteria] + 1e-10),
             color=color_actual, 
             linestyle='-', 
             linewidth=2,
             label=f'{bacteria} (individual)')

    # Graficar datos de la Comunidad (Línea Punteada)
    plt.plot(tiempo_com, np.log10(df_com[bacteria] + 1e-10),
             color=color_actual, 
             linestyle='--', 
             linewidth=2,
             alpha=0.7,
             label=f'{bacteria} (community)')

# Estética de la gráfica
plt.xlabel('Time (h)', fontsize=14)
plt.ylabel(r'Biomass [$\log_{10}$(g)]', fontsize=14)
#plt.title('Comparación de Crecimiento: Unificado vs Comunidad 1', fontsize=16)
plt.grid(True, linestyle=':', alpha=0.6)

# Colocar la leyenda fuera para que no estorbe las curvas
plt.legend(title='Strain ID', bbox_to_anchor=(1.05, 1), loc='upper right', fontsize=10)

# ---------------------------------------------------------
# 4. Guardar y Mostrar
# ---------------------------------------------------------
filename = "comparativa_unificada_vs_comunidad1.png"
plt.savefig(os.path.join(output_path, filename), dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Gráfica comparativa generada con {len(bacterias_comunes)} bacterias.")