import pickle
import os
import pandas as pd
import glob


def process_comets(folder_pkl, output_folder, time_step=0.1):
    os.makedirs(output_folder, exist_ok=True)
    
    pkl_files = glob.glob(os.path.join(folder_pkl, "sim*.pkl"))

    for path_pkl in pkl_files:
        try:
            # Extraer el nombre base (ej: comunidad1)
            nombre_base = os.path.basename(path_pkl).replace('.pkl', '')
            
            with open(path_pkl, 'rb') as file:
                # Cargamos el objeto (resultado de experiment.run())
                experiment_run = pickle.load(file)

            # --- 1. PROCESAR BIOMASA ---
            final_models = experiment_run.total_biomass
            
            if final_models is not None and not final_models.empty:
                # Calculamos tiempo real
                final_models['t'] = final_models['cycle'] * time_step
                
                # Guardar CSV de biomasa
                csv_biomasa = os.path.join(output_folder, f"{nombre_base}_biomasa.csv")
                final_models.to_csv(csv_biomasa, index=False)
                print(f"Procesado: {nombre_base} (Biomasa)")
            
            # --- 2. PROCESAR METABOLITOS ---
            df_metabolites = experiment_run.get_metabolite_time_series()
            if df_metabolites is not None:
                csv_metabolitos = os.path.join(output_folder, f"{nombre_base}_metabolitos.csv")
                df_metabolites.to_csv(csv_metabolitos, index=False)
                print(f"Procesado: {nombre_base} (Metabolitos)")

        except Exception as e:
            print(f"Error en {path_pkl}: {e}")
