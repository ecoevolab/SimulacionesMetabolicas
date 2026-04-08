import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 

def (ruta_csv_syncoms, patron_xml, 
                             threads, cycles, mass, media, folder_resultados):
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
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- LOOP SIMULACION ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):    
        test_tube = c.layout()
        print(f"\n>>> Procesando Comunidad {num}...")

        try:
            # Cargar modelos 
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
            experiment = c.comets(test_tube, sim_params)
            experiment.run(delete_files=False)

            # --- ARCHIVOS GENERADOS POR COMETS ---
            biomass_log = "total_biomass_log.txt"
            media_log = "media_log.txt"
            flux_log = "flux_log.txt"

            # --- GUARDAR RESULTADOS ---
            if os.path.exists(biomass_log):
                output_biomass = os.path.join(folder_resultados, f"biomass_{num}.txt")
                os.rename(biomass_log, output_biomass)
            
            if os.path.exists(media_log):
                output_media = os.path.join(folder_resultados, f"media_{num}.txt")
                os.rename(media_log, output_media)
            
            if os.path.exists(flux_log):
                output_flux = os.path.join(folder_resultados, f"flux_{num}.txt")
                os.rename(flux_log, output_flux)

        except Exception as e:
            print(f"Error en comunidad {num}: {e}")
