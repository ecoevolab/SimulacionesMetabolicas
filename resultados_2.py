import cometspy as c
import cobra.io
import pandas as pd
import os
import glob
import pickle

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, 
           folder_temp, folder_experiment):
    
    # --- PREPARACIÓN DE DIRECTORIOS ---
    os.makedirs(folder_temp, exist_ok=True)
   # os.makedirs(folder_resultados, exist_ok=True)
    os.makedirs(folder_experiment, exist_ok=True)
    
    os.chdir(folder_temp)
    print(f"Directorio de trabajo actual: {os.getcwd()}")

    # --- PARÁMETROS GLOBALES ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    sim_params.set_param('writeMediaLog', True)
    sim_params.set_param('MediaLogRate', 1)
    sim_params.set_param('writeTotalBiomassLog', True)
    sim_params.set_param('writeFluxLog', True)
    sim_params.set_param('FluxLogRate', 1)
    
    initial_mass = [0, 0, mass]

    # --- SELECCIONAR COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_bacterias = df.iloc[:, 0].tolist()
    matriz_ensayos = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_ensayos:
        presentes = [nombre for nombre, valor in zip(id_bacterias, ensayo) if valor == 1]
        comunidades_finales.append(presentes)

    # --- CARGAR MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    for path in lista_archivos:
        model_id = os.path.basename(path).split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path)
        except Exception as e:
            print(f"Error cargando {model_id}: {e}")

    # --- CICLO DE SIMULACIÓN ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):
        print(f"\n>>> Procesando Comunidad {num}: {lista_nombres}")
        try:
            test_tube = c.layout()
            
            # Cargar modelos en el layout
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)

            # Configurar Medio de Cultivo
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except: continue

            trace_met = ['ca2_e','cl_e','cobalt2_e','cu2_e','fe2_e','fe3_e','h_e','k_e','h2o_e',
                         'mg2_e','mn2_e','mobd_e','na1_e','ni2_e','nh4_e','o2_e','pi_e','so4_e','zn2_e']
            for m in trace_met:
                if m not in media:
                    test_tube.set_specific_metabolite(m, 1000)
                test_tube.set_specific_static(m, 1000)

            # --- EJECUTAR SIMULACIÓN ---
            experimet_obj = c.comets(test_tube, sim_params)
            # CAPTURA CRUCIAL: Asignar a variable
            simulation_res = experimet_obj.run() 

            # --- GUARDAR OBJETO (.pkl) ---
            sim_file_path = os.path.join(folder_experiment, f"comunidad_{num}.pkl")
            with open(sim_file_path, 'wb') as file:
                pickle.dump(simulation_res, file)
            
            print(f"Éxito: Comunidad {num} guardada en {sim_file_path}")

        except Exception as e:
            print(f"FALLO en Comunidad {num}: {e}")
