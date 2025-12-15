import pandas as pd
import numpy as np
import glob
import os

comu_path = glob.glob('./04_resultados/rizo/biomasas/comunidad_*.csv')
output_folder = './04_resultados/rizo/biomasas'

for comunidad in comu_path:
    comu_name = os.path.basename(comunidad)
    comu_id = comu_name.replace('.csv', '')

    try:
        df = pd.read_csv(comunidad)

        # Sumar todas las columnas excepto la primera (tiempo)
        df["row_sum"] = df.iloc[:, 1:].sum(axis=1)

        csv_file_name = os.path.join(output_folder, f"{comu_id}_biomasa_suma.csv")
        df.to_csv(csv_file_name, index=False)

    except Exception as e:
        print(f"ADVERTENCIA: Falló el procesamiento de {comu_id}: {e}. Archivo: {comu_name}")

    finally:
        if df is None:
            print(f"--- Iteración {comu_id} finalizada. Estado: FALLO DE SIMULACIÓN/NO REGISTRADO ---")
        else:
            print(f"--- Iteración {comu_id} finalizada correctamente. ---")
