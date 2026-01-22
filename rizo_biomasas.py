# -------------------------------------------
# Genoma anotado en dimont, prokka o eggnog y GEM recostruido en carveme
# ---------------------------------------------
# Cargar paqutes 
import cometspy as c
import cobra.io
import pandas as pd #libreria para manejar tablas
import os # crear carpetas y ''extraer'' nombres 
import glob # para seleccionar varios archivos
# --------------------------
# Cargar variables, rutas y parametros
# Diccionarios para almacenar datos mas adelante
all_models = {} 
# Parametors de la simulación
initial_mass = [0, 0, 5e-8]
sim_params = c.params()
sim_params.set_param('maxCycles', 240)

# Parametro lb
perc_lb = 1

# Datos
dimont_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_dimont_carveme_lb.xml'))
eggnoge_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_eggnog_carveme_lb.xml'))
prokka_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_prokka_carveme_lb.xml'))

model_paths = [dimont_carve, eggnoge_carve, prokka_carve]
# Salida de datos   
csv_output_path = '04_resultados/rizo/biomasa'
os.makedirs(csv_output_path, exist_ok=True)
# ----------------------------
# Ciclo for
for grupo in model_paths: 
    for model_path in grupo:
        file_name = os.path.basename(model_path) # extraer nombre del archivo
        model_id = file_name.replace('.xml', '') # sustituit la ultima parte para cambiar nombre
        if '-draft' in file_name: 
            continue
        
        try:          
            # Cargar modelos y procesarlos                       
            cobra_models = cobra.io.read_sbml_model(model_path)
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
            csv_file_name = os.path.join(csv_output_path, f"{model_id}_lb.csv") # ruta y nombre del archivo 
            final_models.to_csv(csv_file_name, index=False) # gusrad como cvs

            
        except Exception as e:
            print(f"{model_id}: {e}.")


