import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import csv
import pandas as pd
import matplotlib.pyplot as plt
import csv


all_models = {} 
model_summary_data = []
model_reactions = {} 
csv_output_path = '04_resultados/rizo/reacciones'

path_list = glob.glob('02_data/rizo/carveme/ST*_eggnog_carveme_lb.xml')
# ----------------------------

# Ciclo for
for model_path in path_list:
    
    # 1. Extraction and setup
    file_name = os.path.basename(model_path)
    model_id = file_name.replace('.xml', '') 
    
    if '-draft' in file_name:
        continue 
    
    try: 
        # 2. Loading and processing
        cobra_models = cobra.io.read_sbml_model(model_path)
        processed_models = c.model(cobra_models) 

        # 3. Store data (CORRECCIÓN CLAVE EN ESTE BLOQUE)
        
        # Guardar el objeto modelo completo
        all_models[model_id] = processed_models 
        
        # Guardar el conteo de reacciones en una VARIABLE TEMPORAL
        number_of_reactions = len(processed_models.reactions)
        
        # Registrar el conteo en el DICCIONARIO model_reactions
        model_reactions[model_id] = number_of_reactions 
        
        print(f"Modelo {model_id} cargado. Total de reacciones: {number_of_reactions}")

        # ... (el resto del código de simulación) ...
        
    except Exception as e:
        print(f"ERROR: Failed to process model {model_id} from {file_name}. Error: {e}")


# --- REPORTE FINAL (CORRECTO) ---

final_counts_df = pd.DataFrame(
    model_reactions.items(), # .items() solo funciona porque model_reactions es un dict.
    columns=['Model ID', 'Total Reactions']
)

print("\n========================================================")
print("RESUMEN DE CONTEO DE REACCIONES POR MODELO")
print("========================================================")

print(final_counts_df.to_string())

# 2. GUARDAR EL CSV CONSOLIDADO
summary_csv_path = os.path.join(csv_output_path, "reacciones_totales_.csv")

if not final_counts_df.empty:
    final_counts_df.to_csv(summary_csv_path, index=False)