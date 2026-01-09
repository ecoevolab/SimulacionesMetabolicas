# -------------------------------------------------------------
# Cargar librerias
import pandas as pd #para crear tablas y leer archivos csv
import glob #para importar todos los datos de una carpeta
import os #para nombrar los archivos 
# -------------------------------------------------------------
# Seleccionar mis datos
comu_path = glob.glob('./04_resultados/rizo/biomasas/comunidad_*.csv')
output_folder = './04_resultados/rizo/biomasas'
# -------------------------------------------------------------
# Ciclo for 
for comunidad in comu_path:
    comu_name = os.path.basename(comunidad)
    comu_id = comu_name.replace('.csv', '')

    try:
        df = pd.read_csv(comunidad)

        # Sumar todas las columnas excepto la primera (tiempo)
        df["row_sum"] = df.iloc[:, 1:].sum(axis=1)

        # Renombrar los archivos de salida
        csv_file_name = os.path.join(output_folder, f"{comu_id}_biomasa_suma.csv")
        df.to_csv(csv_file_name, index=False)

    except Exception as e:
        print(f"Falló la {comu_id}: {e}")
    else:
        print(f"Lista la {comu_id}")

    