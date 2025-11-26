import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import csv

csv_output_path = '04_resultados/rizo/reacciones'

path_list_prokka = glob.glob('02_data/rizo/carveme/ST*_prokka_carveme_lb.xml')
path_list_eggnog = glob.glob('02_data/rizo/carveme/ST*_eggnog_carveme_lb.xml')
path_list_dimont = glob.glob('02_data/rizo/carveme/ST*_dimont_carveme_lb.xml')

all_models_prokka = {} 
all_model_prokka = {}
model_summary_data_prokka = {}
model_reactions_prokka = {} 
model_metabolites_prokka = {}
model_genes_prokka = {}
# ----------------------------

# Ciclo for
for model_path_prokka in path_list_prokka:
    
    # 1. Extraction and setup
    file_name_prokka = os.path.basename(model_path_prokka)
    model_id_prokka = file_name_prokka.replace('.xml', '') 
    
    if '-draft' in file_name_prokka:
        continue 
    
    try: 
        # 2. Loading and processing
        cobra_models_prokka = cobra.io.read_sbml_model(model_path_prokka)
        #all_model[model_id] = cobra_models
        #processed_models = c.model(cobra_models) 

        # 3. Store data (CORRECCIÓN CLAVE EN ESTE BLOQUE)
        
        # Guardar el objeto modelo completo
        all_models_prokka [model_id_prokka] = cobra_models_prokka 
        
        # Guardar el conteo de reacciones en una VARIABLE TEMPORAL
        number_of_reactions = len(cobra_models_prokka.reactions)
        number_of_metabolites = len(cobra_models_prokka.metabolites)
        number_of_genes = len(cobra_models_prokka.genes)

                # Registrar el conteo en el DICCIONARIO model_reactions
        model_reactions_prokka[model_id_prokka ] = number_of_reactions 
        model_metabolites_prokka [model_id_prokka ] = number_of_metabolites
        model_genes_prokka [model_id_prokka ] = number_of_genes
        print(f"Modelo {model_id_prokka } cargado. Total de reacciones: {number_of_reactions}")
        print(f"Modelo {model_id_prokka } cargado. Total de reacciones: {number_of_metabolites}")
        print(f"Modelo {model_id_prokka } cargado. Total de reacciones: {number_of_genes}")



        # ... (el resto del código de simulación) ...
        
    except Exception as e:
        print(f"ERROR: Failed to process model {model_id_prokka } from {file_name_prokka }. Error: {e}")


# --- REPORTE FINAL (CORRECTO) ---

reactions_df_prokka = pd.DataFrame(
    model_reactions_prokka .items(),
    columns=['Model ID', 'Total Reactions']
)

metabolities_df_prokka = pd.DataFrame(
    model_metabolites_prokka.items(), # .items() solo funciona porque model_reactions es un dict.
    columns=['Model ID', 'Total Metabolites']
)

genes_df_prokka = pd.DataFrame(
    model_genes_prokka.items(), # .items() solo funciona porque model_reactions es un dict.
    columns=['Model ID', 'Total Metabolites']
)

# 2. FUSIONAR las dos tablas por la clave 'Model ID'
counts_df_prokka = pd.merge(
    reactions_df_prokka, 
    metabolities_df_prokka,
    on='Model ID', 
    how='inner' # Asegura que solo se incluyan los modelos que tienen ambos conteos
)


final_counts_df_prokka  = pd.merge(
    counts_df_prokka , 
    genes_df_prokka,
    on='Model ID', 
    how='inner' # Asegura que solo se incluyan los modelos que tienen ambos conteos
)

# 3. GUARDAR EL CSV CONSOLIDADO
summary_csv_path = os.path.join(csv_output_path, "conteo_total_variables_carveme_prokka_lb.csv")
if not final_counts_df_prokka.empty:
    final_counts_df_prokka.to_csv(summary_csv_path, index=False)

# 4. IMPRESIÓN DEL REPORTE FINAL
print("\n========================================================")
print("RESUMEN DE CONTEO DE REACCIONES, METABOLITOS Y GENES")
print("========================================================")

if final_counts_df_prokka.empty:
    print("ADVERTENCIA: El DataFrame de conteo está vacío.")
else:
    print(final_counts_df_prokka.to_string())
    print(f"\nResumen guardado en: {summary_csv_path}")