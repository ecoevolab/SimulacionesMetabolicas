import pandas as pd
import glob
import os

# 1. Buscar todos los archivos CSV en la carpeta
ruta = "./04_resultados/rizo/biomasas/*_prokka_carveme_lb_biomasa_08hrs.csv"
archivos = glob.glob(ruta)

# 2. Lista para almacenar las segundas columnas
columnas_seleccionadas = []

for i, archivo in enumerate(archivos):
    # Leer el CSV
    df = pd.read_csv(archivo)
    
    # Extraer el nombre del archivo para usarlo como encabezado
    nombre_columna = os.path.basename(archivo).replace(".csv", "")
    
    if i == 0:
        # Para el primer archivo, conservamos ambas columnas (ID/Tiempo y Biomasa)
        # Suponiendo que la col 0 es 'cycle' y la col 1 es la biomasa
        df_base = df.iloc[:, [0, 1]]
        df_base.columns = ['ID', nombre_columna]
    else:
        # Para los demás, solo tomamos la segunda columna (índice 1)
        nueva_col = df.iloc[:, [1]]
        nueva_col.columns = [nombre_columna]
        # Unimos horizontalmente
        df_base = pd.concat([df_base, nueva_col], axis=1)

# 3. Guardar el resultado unificado
df_base.to_csv("unificado_biomasas_08.csv", index=False)
print("Archivo unido con éxito.")