# -------------------------------------------------------------------------------------------------
import cometspy as c
import cobra.io
import pandas as pd
import os
import glob

def biomass_comunidades_rizo(ruta_csv_syncoms, patron_xml,
                             threads, cycles, mass, media, folder_resultados):
    # --- PARÁMETROS ---
    sim_params = c.params()
    sim_params.set_param('numRunThreads', threads)
    sim_params.set_param('maxCycles', cycles)
    initial_mass = [0, 0, mass]
    dilution_rate = 0.1
    os.makedirs(folder_resultados, exist_ok=True)

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
            modelos_base = cobra.io.read_sbml_model(path_completo)
    cmd_name = f"{model_id}.cmd"
    cmd_files = os.path.join(folder_resultador, cmd_name)
	with open(full_path, "w") as f:
       # f.write(")
       # f.write("")
        
   # print("")

##########


        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- CICLO DE SIMULACIÓN POR COMUNIDAD ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):    
        test_tube = c.layout()
        print(f"\n>>> Procesando Comunidad {num}...")
        
        try:
            # Cargar modelos de la comunidad desde memoria
            modelos_agregados = []
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                    modelos_agregados.append(model_id)
                else:
                    print(f"No se encontró el {model_id}")

            # ----------------------------------------------------
            # MEDIO DE CULTIVO 
            # ----------------------------------------------------            
            for met, conc in media.items():
                try:
                    test_tube.set_specific_metabolite(met, conc)
                except:
                    pass

            # Mantener los traza estáticos
            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 
                                 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 
                                 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']
            
            for i in trace_metabolites:
                if i not in media:
                    test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)

            # --- EJECUCIÓN ---
            experimet = c.comets(test_tube, sim_params)
            experimet.run()

            # --- RESULTADOS ---
            final_models = experimet.total_biomass
            
            if final_models is not None and not final_models.empty:
                # Calculamos tiempo real antes de renombrar columnas
                final_models['t'] = final_models['cycle'] * experimet.parameters.all_params['timeStep']
                
                # Ajustamos columnas (cycle + nombres de bacterias + t)
                final_models.columns = ['cycle'] + modelos_agregados + ['t']
                
                csv_file_name = os.path.join(folder_resultados, f"comunidad_{num}.csv")
                final_models.to_csv(csv_file_name, index=False)
                print(f"Comunidad {num} guardada con éxito.")
            else:
                print(f"Comunidad {num} terminó sin biomasa.")

        except Exception as e:
            print(f"Falló Comunidad {num}: {e}")
