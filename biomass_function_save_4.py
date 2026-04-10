import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, newpath):
    # 1. Guardar la ruta donde se ejecuta el script (para poder volver al final)
    original_path = os.getcwd()
    
    # 2. Crear y entrar a la carpeta principal de resultados (ruta absoluta)
    root_path = os.path.abspath(newpath)
    os.makedirs(root_path, exist_ok=True)
    
    # --- CARGAR DATOS DE COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_bacterias = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_bacterias, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- CARGAR MODELOS A MEMORIA ---
    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        model_id = archivo.split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- PARAMETROS DE SIMULACIÓN ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    sim_params.set_param('writeMediaLog', True)
    sim_params.set_param('MediaLogRate', 1)
    sim_params.set_param('writeTotalBiomassLog', True)
    sim_params.set_param('writeFluxLog', True)
    sim_params.set_param('FluxLogRate', 1)

    initial_mass = [0, 0, mass]

    # --- LOOP DE SIMULACIÓN ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):
        # MUY IMPORTANTE: Regresar a la raíz de resultados en cada vuelta
        os.chdir(root_path)
        
        folder_name = f"Comunidad_{num}"
        os.makedirs(folder_name, exist_ok=True)
        
        # Entrar a la carpeta de la comunidad actual
        os.chdir(folder_name)
        current_community_dir = os.getcwd()
        
        print(f"\n>>> Simulando Comunidad {num} en: {current_community_dir}")

        try:
            test_tube = c.layout()
            
            # Cargar los modelos específicos de esta comunidad
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                else:
                    print(f"Advertencia: {model_id} no está en los archivos XML")

            # --- CONFIGURAR MEDIO DE CULTIVO --- 
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
                    try:
                        test_tube.set_specific_metabolite(i, 1000)
                    except:
                        pass
                test_tube.set_specific_static(i, 1000)

            # --- EJECUTAR COMETS ---
            experiment = c.comets(test_tube, sim_params)
            
            # Al haber usado os.chdir(), COMETS escribirá aquí automáticamente
            experiment.run(delete_files=False)
            
            print(f"Comunidad {num} finalizada con éxito.")

        except Exception as e:
            print(f"Error en Comunidad {num}: {e}")

    # 3. Al terminar todo el loop, volver a la carpeta original del script
    os.chdir(original_path)
    print("\nProceso completo. Todos los resultados están en:", root_path)