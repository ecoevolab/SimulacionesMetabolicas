import cometspy as c
import cobra.io
import pandas as pd
import os
import glob 
import multiprocessing as mp

# --- FUNCIÓN DE TRABAJO (La que ejecutará cada proceso) ---
def worker_simulacion(num, lista_nombres, modelos_base, sim_params, folder_resultados, initial_mass):
    """
    Esta función corre la simulación para una sola comunidad.
    """
    try:
        test_tube = c.layout()
        print(f">>> Procesando Comunidad {num} en paralelo...")
        
        for model_id in lista_nombres:
            if model_id in modelos_base:
                # Importante: Copia profunda para evitar colisiones entre procesos
                cobra_copy = modelos_base[model_id].copy()
                processed_model = c.model(cobra_copy)
                processed_model.initial_pop = initial_mass
                test_tube.add_model(processed_model)
            else:
                print(f"No se encontró el {model_id}")

            # ----------------------------------------------------
            # MEDIO DE CULTIVO 
            # ----------------------------------------------------
            test_tube.set_specific_metabolite("h2o_e", 100)
            test_tube.set_specific_metabolite("o2_e", 10)
            test_tube.set_specific_metabolite("pi_e", 100)
            test_tube.set_specific_metabolite("prbamp_e", 100)
            test_tube.set_specific_metabolite("glu__L_e", 1)
            test_tube.set_specific_metabolite("mn2_e", 100)
            test_tube.set_specific_metabolite("gly_e", 1)
            test_tube.set_specific_metabolite("zn2_e", 100)
            test_tube.set_specific_metabolite("ala__L_e", 1)
            test_tube.set_specific_metabolite("lys__L_e", 1)
            test_tube.set_specific_metabolite("asp__L_e", 1)
            test_tube.set_specific_metabolite("so4_e", 1)
            test_tube.set_specific_metabolite("arg__L_e", 1)
            test_tube.set_specific_metabolite("ser__L_e", 1)
            test_tube.set_specific_metabolite("cu2_e", 1)
            test_tube.set_specific_metabolite("met__L_e", 1)
            test_tube.set_specific_metabolite("trp__L_e", 1)
            test_tube.set_specific_metabolite("phe__L_e", 1)
            test_tube.set_specific_metabolite("h_e", 1)
            test_tube.set_specific_metabolite("tyr__L_e", 1)
            test_tube.set_specific_metabolite("cys__L_e", 1)
            test_tube.set_specific_metabolite("ura_e", 1)
            test_tube.set_specific_metabolite("cl_e", 1)
            test_tube.set_specific_metabolite("leu__L_e", 1)
            test_tube.set_specific_metabolite("his__L_e", 1)
            test_tube.set_specific_metabolite("pro__L_e", 1)
            test_tube.set_specific_metabolite("cobalt2_e", 100)
            test_tube.set_specific_metabolite("val__L_e", 1)
            test_tube.set_specific_metabolite("thr__L_e", 1)
            test_tube.set_specific_metabolite("adn_e", 0.1)
            test_tube.set_specific_metabolite("thymd_e", 0.1)
            test_tube.set_specific_metabolite("k_e", 100)
            test_tube.set_specific_metabolite("h2s_e", 0.1)
            test_tube.set_specific_metabolite("ins_e", 0.1)
            test_tube.set_specific_metabolite("uri_e", 0.1)
            test_tube.set_specific_metabolite("mg2_e", 100)
            test_tube.set_specific_metabolite("gsn_e", 0.1)
            test_tube.set_specific_metabolite("ile__L_e", 1)
            test_tube.set_specific_metabolite("skm_e", 1)
            test_tube.set_specific_metabolite("fol_e", 1)
            test_tube.set_specific_metabolite("dadn_e", 1)
            test_tube.set_specific_metabolite("lipoate_e", 0.1)
            test_tube.set_specific_metabolite("na1_e", 100)
            test_tube.set_specific_metabolite("cd2_e", 100)
            test_tube.set_specific_metabolite("aso4_e", 100)
            test_tube.set_specific_metabolite("fe2_e", 100)
            test_tube.set_specific_metabolite("fe3_e", 100)
            test_tube.set_specific_metabolite("cro4_e", 100)
            test_tube.set_specific_metabolite("nh3_c_e", 100)
            test_tube.set_specific_metabolite("pheme_e", 100)
            test_tube.set_specific_metabolite("cmp_e", 100)
            test_tube.set_specific_metabolite("ump_e", 100)
            test_tube.set_specific_metabolite("gmp_e", 100)
            test_tube.set_specific_metabolite("pydx_e", 100)
            test_tube.set_specific_metabolite("nac_e", 100)
            test_tube.set_specific_metabolite("ribflv_e", 100)
            test_tube.set_specific_metabolite("pphn_e", 100)
            test_tube.set_specific_metabolite("hxan_e", 100)
            test_tube.set_specific_metabolite("thmpp_e", 0.1)
            test_tube.set_specific_metabolite("cbl1_e", 0.1)

            trace_metabolites = [
                'ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e',
                'h_e', 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e',
                'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e'
            ]

            for i in trace_metabolites:
                test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)

        experimet = c.comets(test_tube, sim_params)
        experimet.run()

        final_models = experimet.total_biomass
        if final_models is not None and not final_models.empty:
            final_models.columns = ['cycle'] + lista_nombres
            csv_file_name = os.path.join(folder_resultados, f"comunidad_{num}.csv")
            final_models.to_csv(csv_file_name, index=False)
            return f"Comunidad {num}: Éxito"
        else:
            return f"Comunidad {num}: Sin biomasa"
            
    except Exception as e:
        return f"Comunidad {num}: Error -> {e}"

# --- FUNCIÓN PRINCIPAL REESTRUCTURADA ---
def biomass_comunidades_rizo_parallel(ruta_csv_syncoms, patron_xml, folder_resultados):
    # 1. Configuración inicial
    sim_params = c.params()
    sim_params.set_param('numRunThreads', 3) # IMPORTANTE: 1 thread interno si usas multiprocessing
    sim_params.set_param('maxCycles', 80)
    initial_mass = [0, 0, 5e-8]
    os.makedirs(folder_resultados, exist_ok=True)

    # 2. Cargar datos y modelos (esto se hace una sola vez)
    df = pd.read_csv(ruta_csv_syncoms)
    id_comunidad = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()
    
    comunidades_finales = [[nombre for nombre, valor in zip(id_comunidad, ensayo) if valor == 1] 
                          for ensayo in matriz_bacterias]

    modelos_base = {}
    lista_archivos = glob.glob(patron_xml)
    for path_completo in lista_archivos:
        model_id = os.path.basename(path_completo).split('_')[0]
        modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)

    # 3. LANZAR MULTIPROCESSING
    # Definimos cuántos procesos simultáneos queremos (ej: 4)
    num_procesos = mp.cpu_count() - 1 # Usa casi todos tus núcleos
    
    with mp.Pool(processes=num_procesos) as pool:
        # Preparamos los argumentos para cada llamado a la función worker
        args = [(num, lista, modelos_base, sim_params, folder_resultados, initial_mass) 
                for num, lista in enumerate(comunidades_finales, start=1)]
        
        # starmap distribuye el trabajo
        resultados = pool.starmap(worker_simulacion, args)

    for r in resultados:
        print(r)

# --- BLOQUE DE EJECUCIÓN SEGURO ---
if __name__ == '__main__':
    # Configuración para el clúster/Linux
    mp.set_start_method('spawn', force=True)
    
    # Rutas de ejemplo (ajusta a tus rutas de /mnt/data/sur/...)
    mi_ruta_csv = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/syncoms.csv"
    mi_patron_xml = "/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/carveme/ST*_prokka_carveme_lb.xml"
    mi_output = "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomasas"
    
    biomass_comunidades_rizo_parallel(mi_ruta_csv, mi_patron_xml, mi_output)