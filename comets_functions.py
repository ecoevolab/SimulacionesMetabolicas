import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def comets(ruta_csv_syncoms, patron_xml, threads, cycles, mass, media, newpath):
    # 1. Guardar la ruta original (donde está tu script)
    original_path = os.getcwd()
    
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
        # VOLVER A LA RAÍZ de resultados para evitar anidamiento
        os.chdir(root_path)
        
        folder_name = f"comunidad_{num}"
        os.makedirs(folder_name, exist_ok=True)
        
        # ENTRAR a la carpeta de la comunidad actual
        os.chdir(folder_name)
        
        print(f"\n>>> Simulando Comunidad {num} en: {os.getcwd()}")

        try:
            test_tube = c.layout()
            
            # Cargar modelos y guardar sus nombres para las columnas del CSV
            modelos_agregados = []
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                    modelos_agregados.append(model_id) # Se guarda para el encabezado del CSV
                else:
                    print(f"Advertencia: {model_id} no encontrado en archivos XML")

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
            # Al haber usado os.chdir(), COMETS escribe aquí por defecto
            experiment.run(delete_files=False)
            
            # --- PROCESAR Y GUARDAR RESULTADOS ---
            final_models = experiment.total_biomass

            if final_models is not None and not final_models.empty:
                # Calcular tiempo real (ciclos * timeStep)
                time_step = experiment.parameters.all_params['timeStep']
                final_models['t'] = final_models['cycle'] * time_step
                
                # Ajustar nombres de columnas: 'cycle' + nombres bacterias + 't'
                final_models.columns = ['cycle'] + modelos_agregados + ['t']

                # Guardar CSV (ya estamos dentro de Comunidad_X)
                final_models.to_csv(f"comunidad_{num}_biomasa.csv", index=False)
                print(f"Biomasa guardada exitosamente.")
            
            # Guardar metabolitos
            df_metabolites = experiment.get_metabolite_time_series()
            if df_metabolites is not None:
                df_metabolites.to_csv(f"comunidad_{num}_metabolitos.csv", index=False)
                print(f"Metabolitos guardados exitosamente.")

            # Guardar media log
            media_log = experiment.media

            if media_log is not None and not media_log.empty:
                media_log.to_csv(f"comunidad_{num}_media.csv", index=False)
                print("Media log guardado exitosamente.")

        except Exception as e:
            print(f"Error crítico en Comunidad {num}: {e}")

    # 3. Al finalizar, volver a la carpeta donde empezamos
    os.chdir(original_path)
    print(f"\nProceso finalizado. Resultados en: {root_path}")

def media(name = "lb", dil = 1):
    if name == "lb":
       res = {
            "h2o_e": 100*dil, "o2_e": 10*dil, "pi_e": 10*dil, "zn2_e": 10, 
            "cobalt2_e": 10*dil, "k_e": 10*dil, "mg2_e": 10*dil, "na1_e": 10*dil, "cd2_e": 10*dil, 
            "aso4_e": 10*dil, "fe2_e": 10*dil, "fe3_e": 10*dil, "cro4_e": 10*dil, 
            "pydx_e": 10*dil, "nac_e": 10*dil, "ribflv_e": 10*dil, "ura_e": 0.1*dil,
            "glu__L_e": 0.1*dil, "gly_e": 0.1*dil,
            "ala__L_e": 0.1*dil, "lys__L_e": 0.1*dil, 
            "asp__L_e": 0.1*dil, "so4_e": 0.1*dil,
            "arg__L_e": 0.1*dil, "ser__L_e": 0.1*dil, 
            "cu2_e": 0.1*dil, "met__L_e": 0.1*dil, 
            "trp__L_e": 0.1*dil, "phe__L_e": 0.1*dil, 
            "h_e": 0.1*dil, "tyr__L_e": 0.1*dil, 
            "cys__L_e": 0.1*dil, "cl_e": 0.1*dil, 
            "leu__L_e": 0.1*dil, "his__L_e": 0.1*dil, 
            "pro__L_e": 0.1*dil, "val__L_e": 0.1*dil, 
            "thr__L_e": 0.1*dil, "ile__L_e": 0.1*dil
        }
    else:
        raise ValueError("Unrecognized media. Currently only 'lb' is supported.")
    
    return res
       

def load_strains(layout, models, initial_mass = 1e-8):
    for strain, gem in models.items():
        # print(f"==============Cargando modelo para {strain} desde {gem}==============")
        gem_i = cobra.io.read_sbml_model(gem)
        # print(f"=========================Modelo cargado para {strain}==============")
        gem_i = c.model(gem_i)
        # print(f"=========================Modelo procesado para {strain}==============")
        gem_i.id = strain
        # print(f"=========================ID establecido para {strain}==============")
        gem_i.initial_pop = [0, 0, initial_mass]
        # print(f"=========================Biomasa inicial para {strain}==============")
        layout.add_model(gem_i)
        # print(f"=========================Modelo añadido {strain}==============")
    
    return layout

    
