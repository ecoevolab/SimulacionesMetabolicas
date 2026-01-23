import cometspy as c
import cobra.io
import pandas as pd
import os

def biomass_cepas_rizo(gems, X, Y, Z, cicles):
    all_models = {} 
    initial_mass = [X, Y, Z]
    sim_params = c.params()
    sim_params.set_param('maxCycles', cicles)
    csv_output_path = '04_resultados/rizo/biomasas'
    os.makedirs(csv_output_path, exist_ok=True)
    for item in gems: 
        file_name = os.path.basename(item) # extraer nombre del archivo
        output_name = file_name.replace('.xml', '') # sustituit la ultima parte para cambiar nombre
        model_id = file_name[:7]
        if not '.xml' in file_name: 
            continue
        
        try:          
            # Cargar modelos y procesarlos                       
            cobra_models = cobra.io.read_sbml_model(item)
            processed_models = c.model(cobra_models) 
            all_models[model_id] = processed_models # guarda cada uno de los modelos procesados
            # Cargar experimento 
            processed_models.initial_pop = initial_mass
            test_tube = c.layout()
            test_tube.add_model(processed_models)

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
            test_tube.set_specific_metabolite("cys__L_e", 1)
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

            # Add typical trace metabolites and oxygen coli as static
            trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 'k_e', 'h2o_e', 'mg2_e',
                                'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

            for i in trace_metabolites:
                test_tube.set_specific_metabolite(i, 1000)
                test_tube.set_specific_static(i, 1000)
        # Cargar simulación
            experimet = c.comets(test_tube, sim_params)
            experimet.run()
            final_models = experimet.total_biomass
            csv_file_name = os.path.join(csv_output_path, f"{output_name}.csv") # ruta y nombre del archivo 
            final_models.to_csv(csv_file_name, index=False) # gusrad como cvs

            
        except Exception as e:
            print(f"{model_id}: {e}.")

import cometspy as c
import cobra.io
import pandas as pd
import os
import glob  # Importante para usar el patrón ST*_prokka

def biomass_comunidades_rizo(ruta_csv_syncoms, patron_xml, folder_resultados):
    """
    patron_xml: debe recibir algo como './02_data/rizo/carveme/*_prokka_carveme_lb.xml'
    """
    # --- 1. CONFIGURACIÓN DE PARÁMETROS ---
    sim_params = c.params()
    sim_params.set_param('maxCycles', 480)
    sim_params.set_param('timeStep', 0.1)
    initial_mass = [0, 0, 5e-8]

    os.makedirs(folder_resultados, exist_ok=True)

    # --- 2. PREPARACIÓN DE COMUNIDADES ---
    df = pd.read_csv(ruta_csv_syncoms)
    id_comunidad = df.iloc[:, 0].tolist()
    matriz_bacterias = df.iloc[:, 1:].astype(int).T.values.tolist()  
    
    comunidades_finales = []
    for ensayo in matriz_bacterias:
        bacterias_presentes = [nombre for nombre, valor in zip(id_comunidad, ensayo) if valor == 1]
        comunidades_finales.append(bacterias_presentes)

    # --- 3. CARGA ÚNICA DE MODELOS A MEMORIA (Usando glob) ---
    modelos_base = {}
    # glob.glob busca todos los archivos que coincidan con tu patrón ST*_prokka...
    lista_archivos = glob.glob(patron_xml)
    
    print(f"Cargando {len(lista_archivos)} modelos SBML a memoria...")
    for path_completo in lista_archivos:
        archivo = os.path.basename(path_completo)
        #model_id = archivo[:7]  # Extrae el ID (ej: ST00046)
        model_id = archivo.split('_')[0]
        try:
            modelos_base[model_id] = cobra.io.read_sbml_model(path_completo)
        except Exception as e:
            print(f"Error cargando {archivo}: {e}")

    # --- 4. CICLO DE SIMULACIÓN POR COMUNIDAD ---
    for num, lista_nombres in enumerate(comunidades_finales, start=1):    
        test_tube = c.layout()
        print(f"\n>>> Procesando Comunidad {num}...")
        
        try:
            # Cargar modelos de la comunidad desde memoria
            for model_id in lista_nombres:
                if model_id in modelos_base:
                    cobra_copy = modelos_base[model_id].copy()
                    processed_model = c.model(cobra_copy)
                    processed_model.initial_pop = initial_mass
                    test_tube.add_model(processed_model)
                else:
                    print(f"⚠️ Alerta: No se encontró el modelo para {model_id} en la carga inicial")

            # ----------------------------------------------------
            # MEDIO DE CULTIVO (Mantenido igual)
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

            # --- EJECUCIÓN ---
            experimet = c.comets(test_tube, sim_params)
            experimet.run()

            final_models = experimet.total_biomass
            if final_models is not None and not final_models.empty:
                final_models.columns = ['cycle'] + lista_nombres
                csv_file_name = os.path.join(folder_resultados, f"comunidad_{num}.csv")
                final_models.to_csv(csv_file_name, index=False)
                print(f"✅ Comunidad {num} guardada con éxito.")
            else:
                print(f"⚠️ Comunidad {num} terminó sin biomasa.")

        except Exception as e:
            print(f"❌ Falló Comunidad {num}: {e}")

