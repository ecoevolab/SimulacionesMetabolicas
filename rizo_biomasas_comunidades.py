import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import csv
from pathlib import Path

# ---------------------------
all_models = {} 
model_summary_data = []
sim_params = c.params()
sim_params.set_param('maxCycles', 80)
sim_params.set_param('timeStep', 0.1)
initial_mass = [0, 0, 5e-8]   
csv_output_path = '04_resultados/rizo/biomasas/'


# ----------------------------------------------
def select_specific_files_os(folder_path, specific_filenames):

    selected_files = []
    
    for filename in specific_filenames:
        # os.path.join handles the correct slash for your OS
        full_path = os.path.join(folder_path, filename) 
        
        # Check if the file exists at that path
        if os.path.isfile(full_path):
            selected_files.append(full_path)
        else:
            print(f"Warning: '{filename}' not found.")
            
    return selected_files

folder_location = "./02_data/rizo/carveme" 

comunidad_1 = ["ST00046_prokka_carveme_lb.xml", "ST00154_prokka_carveme_lb.xml"
                  , "ST00101_prokka_carveme_lb.xml", "ST00109_prokka_carveme_lb.xml", "ST00042_prokka_carveme_lb.xml"]

comunidad_2 = ["ST00046_prokka_carveme_lb.xml", "ST00154_prokka_carveme_lb.xml"
                  , "ST00101_prokka_carveme_lb.xml", "ST00109_prokka_carveme_lb.xml", "ST00060_prokka_carveme_lb.xml"]

comunidad_3 = ["ST00046_prokka_carveme_lb.xml", "ST00154_prokka_carveme_lb.xml"
                  , "ST00101_prokka_carveme_lb.xml", "ST00042_prokka_carveme_lb.xml", "ST00094_prokka_carveme_lb.xml"]

# comunidad_4 = ["ST00046_prokka_carveme_lb.xml", "ST00154_prokka_carveme_lb.xml"
#                   , "ST00109_prokka_carveme_lb.xml", "ST00042_prokka_carveme_lb.xml", "ST00110_prokka_carveme_lb.xml"]

# comunidad_5 = ["ST00046_prokka_carveme_lb.xml", "ST00101_prokka_carveme_lb.xml"
#                   , "ST00109_prokka_carveme_lb.xml", "ST00042_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml"]
# comunidad_6 = ["ST00154_prokka_carveme_lb.xml", "ST00101_prokka_carveme_lb.xml"
#                   , "ST00109_prokka_carveme_lb.xml", "ST00042_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml"]
# #-------------------------------------------------
# comunidad_7 = ["ST00060_prokka_carveme_lb.xml", "ST00094_prokka_carveme_lb.xml"
#                  , "ST00110_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml", "ST00143_prokka_carveme_lb.xml"]
# comunidad_8 = ["ST00042_prokka_carveme_lb.xml", "ST00094_prokka_carveme_lb.xml"
#                  , "ST00110_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml", "ST00143_prokka_carveme_lb.xml"]
# comunidad_9 = ["ST00109_prokka_carveme_lb.xml", "ST00060_prokka_carveme_lb.xml"
#                  , "ST00110_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml", "ST00143_prokka_carveme_lb.xml"]
# comunidad_10 = ["ST00101_prokka_carveme_lb.xml", "ST00060_prokka_carveme_lb.xml"
#                  , "ST00094_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml", "ST00143_prokka_carveme_lb.xml"]
# comunidad_11 = ["ST00154_prokka_carveme_lb.xml", "ST00060_prokka_carveme_lb.xml"
#                  , "ST00094_prokka_carveme_lb.xml", "ST00110_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml"]
# comunidad_12 = ["ST00046_prokka_carveme_lb.xml", "ST00060_prokka_carveme_lb.xml"
#                  , "ST00094_prokka_carveme_lb.xml", "ST00110_prokka_carveme_lb.xml", "ST00164_prokka_carveme_lb.xml"]

found_1 = select_specific_files_os(folder_location, comunidad_1)
found_2 = select_specific_files_os(folder_location, comunidad_2)
found_3 = select_specific_files_os(folder_location, comunidad_3)
# found_4 = select_specific_files_os(folder_location, comunidad_4)
# found_5 = select_specific_files_os(folder_location, comunidad_5)
# found_6 = select_specific_files_os(folder_location, comunidad_6)
# # --------------------------------------------------------------
# found_7 = select_specific_files_os(folder_location, comunidad_7)
# found_8 = select_specific_files_os(folder_location, comunidad_8)
# found_9 = select_specific_files_os(folder_location, comunidad_9)
# found_10 = select_specific_files_os(folder_location, comunidad_10)
# found_11 = select_specific_files_os(folder_location, comunidad_11)
# found_12 = select_specific_files_os(folder_location, comunidad_12)


comunidades = [found_1, found_2, found_3]

print("Found files (full paths):")

# -----------------------------------------------------------

for num, comunidad in enumerate(comunidades, start=3):
    test_tube = c.layout()

    try:
        # ----------------------------------------------------
        # Cargar todos los modelos de la comunidad
        for modelo in comunidad:
            file_name = os.path.basename(modelo)
            model_id = file_name.replace("_prokka_carveme_lb.xml", "")

            cobra_models = cobra.io.read_sbml_model(modelo)
            processed_models = c.model(cobra_models)

            processed_models.initial_pop = initial_mass
            test_tube.add_model(processed_models)

        # ----------------------------------------------------
        # Agregar metabolitos específicos (UNA sola vez)
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

        # ----------------------------------------------------
        trace_metabolites = [
            'ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e',
            'h_e', 'k_e', 'h2o_e', 'mg2_e', 'mn2_e', 'mobd_e',
            'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e'
        ]

        for i in trace_metabolites:
            test_tube.set_specific_metabolite(i, 1000)
            test_tube.set_specific_static(i, 1000)

        # ----------------------------------------------------
        experimet = c.comets(test_tube, sim_params)
        experimet.run()

        final_models = experimet.total_biomass

        if final_models is not None:
            csv_file_name = os.path.join(csv_output_path, f"comunidad_{num}.csv")
            final_models.to_csv(csv_file_name, index=False)

            print(f" {num} registrada")
            print(final_models.to_string())
        else:
            print(f"{num} falló")


    except Exception as e:
        print(f"Falló {num}: {e}")

