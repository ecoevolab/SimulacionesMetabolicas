import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, newpath):
    # Asegurar que el path principal existe y movernos ahí
    root_path = os.path.abspath(newpath) # Usamos ruta absoluta para evitar confusiones
    os.makedirs(root_path, exist_ok=True)
    os.chdir(root_path)

    # --- PARAMETROS ---
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
    id_comunidad = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_comunidad, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- CARGAR MODELOS ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML a memoria...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        model_id = archivo.split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- LOOP SIMULACION ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):    
        # 1. Crear carpeta específica para la comunidad
        folder_name = f"Comunidad_{num}"
        community_path = os.path.join(root_path, folder_name)
        os.makedirs(community_path, exist_ok=True)
        
        test_tube = c.layout()
        print(f"\n>>> Procesando Comunidad {num} en {folder_name}...")

        try:
            # Cargar modelos 
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                else:
                    print(f"No se encontró el {model_id}")

            # ---------------- MEDIO DE CULTIVO --------------------- 
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                                 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                                 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

            for i in trace_metabolites:
                if i not in media:
                    test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)

            # --- SIMULACION  ---
            # 2. Pasar el community_path a la simulación
            experiment = c.comets(test_tube, sim_params)
            
            # El parámetro working_dir hace que COMETS escriba los .txt allí
            experiment.working_dir = community_path 
            
            experiment.run(delete_files=False)
            
            # 3. Guardar opcionalmente los dataframes como CSV en esa carpeta
            experiment.total_biomass.to_csv(os.path.join(community_path, "biomass.csv"))
            experiment.get_metabolite_time_series().to_csv(os.path.join(community_path, "metabolites.csv"))

            print(f"Simulación {num} completada exitosamente.")

        except Exception as e:
            print(f"Error en comunidad {num}: {e}")