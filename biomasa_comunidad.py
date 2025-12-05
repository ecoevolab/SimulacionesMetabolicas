#Start by loading required packages, including the COMETS toolbox
import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import os 
import matplotlib.cm as cm 
import math


ST42 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00042_prokka_carveme_lb.xml'))
ST42.id = 'Pumsongensis'
# ST46 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00046_prokka_carveme_lb.xml'))
# ST46.id = 'Bacillus'
# ST101 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00094_prokka_carveme_lb.xml'))
# ST101.id = 'Pseudomonas'
# ST109 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00109_prokka_carveme_lb.xml'))
# ST109.id = 'Mycobacterium'
# ST154 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00110_prokka_carveme_lb.xml'))
# ST154.id = 'Agrobacterium'

csv_output_path = '04_resultados/rizo/biomasas'
model_summary_data = []


# set its initial biomass, 5e-6 gr at coordinate [0,0]
ST42.initial_pop = [0, 0, 5e-8]
# ST46.initial_pop = [0, 0, 5e-8]
# ST101.initial_pop = [0, 0, 5e-8]
# ST109.initial_pop = [0, 0, 5e-8]
# ST154.initial_pop = [0, 0, 5e-8]

# create an empty layout
test_tube = c.layout()

# add the models to the test tube
test_tube.add_model(ST42)
# test_tube.add_model(ST46)
# test_tube.add_model(ST101)
# test_tube.add_model(ST109)
# test_tube.add_model(ST154)

test_tube.set_specific_metabolite("h2o_e", 100)
test_tube.set_specific_metabolite("o2_e", 10)
test_tube.set_specific_metabolite("pi_e", 10)
test_tube.set_specific_metabolite("prbamp_e", 10)
test_tube.set_specific_metabolite("glu__L_e", 0.1)
test_tube.set_specific_metabolite("mg2_e", 0.1)
test_tube.set_specific_metabolite("gly_e", 0.1)
test_tube.set_specific_metabolite("zn2_e", 10)
test_tube.set_specific_metabolite("ala__L_e", 0.1)
test_tube.set_specific_metabolite("lys__L_e", 0.1)
test_tube.set_specific_metabolite("asp__L_e", 0.1)
test_tube.set_specific_metabolite("so4_e", 0.1)
test_tube.set_specific_metabolite("arg__L_e", 0.1)
test_tube.set_specific_metabolite("ser__L_e", 0.1)
test_tube.set_specific_metabolite("cu2_e", 0.1)
test_tube.set_specific_metabolite("met__L_e", 0.1)
test_tube.set_specific_metabolite("trp__L_e", 0.1)
test_tube.set_specific_metabolite("phe__L_e", 0.1)
test_tube.set_specific_metabolite("h_e", 0.1)
test_tube.set_specific_metabolite("tyr__L_e", 0.1)
test_tube.set_specific_metabolite("cys__L_e", 0.1)
test_tube.set_specific_metabolite("ura_e", 0.1)
test_tube.set_specific_metabolite("cl_e", 0.1)
test_tube.set_specific_metabolite("leu__L_e", 0.1) 
test_tube.set_specific_metabolite("his__L_e", 0.1)
test_tube.set_specific_metabolite("pro__L_e", 0.1)
test_tube.set_specific_metabolite("cobalt2_e", 10)
test_tube.set_specific_metabolite("val__L_e", 0.1)
test_tube.set_specific_metabolite("thr__L_e", 0.1)
test_tube.set_specific_metabolite("adn_e", 0.01)
test_tube.set_specific_metabolite("thymd_e", 0.01)
test_tube.set_specific_metabolite("k_e", 10)
test_tube.set_specific_metabolite("h2s_e", 0.01)
test_tube.set_specific_metabolite("ins_e", 0.01)
test_tube.set_specific_metabolite("uri_e", 0.01)
test_tube.set_specific_metabolite("mg2_e", 10)
test_tube.set_specific_metabolite("gsn_e", 0.01)
test_tube.set_specific_metabolite("ile__L_e", 0.1)
test_tube.set_specific_metabolite("cys__L_e", 0.1)
test_tube.set_specific_metabolite("skm_e", 0.01)
test_tube.set_specific_metabolite("fol_e", 0.01)
test_tube.set_specific_metabolite("dadn_e", 0.01)
test_tube.set_specific_metabolite("lipoate_e", 0.01)
test_tube.set_specific_metabolite("na1_e", 10)
test_tube.set_specific_metabolite("cd2_e", 10)
test_tube.set_specific_metabolite("aso4_e", 10)
test_tube.set_specific_metabolite("fe2_e", 10)
test_tube.set_specific_metabolite("fe3_e", 10)
test_tube.set_specific_metabolite("cro4_e", 10)
test_tube.set_specific_metabolite("nh3_c", 10)
test_tube.set_specific_metabolite("pheme", 10)
test_tube.set_specific_metabolite("cmp", 10)
test_tube.set_specific_metabolite("ump", 10)
test_tube.set_specific_metabolite("gmp", 10)
test_tube.set_specific_metabolite("pydx", 10)
test_tube.set_specific_metabolite("nac", 10)
test_tube.set_specific_metabolite("ribflv", 10)
test_tube.set_specific_metabolite("pphn", 10)
test_tube.set_specific_metabolite("hxan", 10)

# Add typical trace metabolites and oxygen coli as static
trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 'k_e', 'h2o_e', 'mg2_e',
                     'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

for i in trace_metabolites:
    test_tube.set_specific_metabolite(i, 1000)
    test_tube.set_specific_static(i, 1000)

comp_params = c.params()
# Set the time step (e.g., 60 seconds per cycle)

#comp_params.set_param('timeStep', 0.01) #cuando tiempo 
comp_params.set_param('timeStep', 0.1)
comp_params.set_param('maxCycles', 80)

comp_assay = c.comets(test_tube, comp_params)
comp_assay.run()

# final_models = comp_assay.total_biomass
# print(final_models)

# csv_file_name = os.path.join(csv_output_path, "biomasa_comunidad.csv")
# final_models.to_csv(csv_file_name, index=False)



# df_biomasas = pd.read_csv('./04_resultados/rizo/biomasas/biomasa_comunidad.csv')
# #df_biomasas_final = df_biomasas.drop('columna1', axis=1)

# # df_cycles = pd.DataFrame({
# #     "cycles": range(1, 81)
# # })

# out_folder = './04_resultados/rizo/biomasas'

# for i in df_biomasas.columns[1:]:
#     sub_df = df_biomasas[['cycle', i]]  
#     nombre = f"{out_folder}/{i}_bueno.csv"
#     sub_df.to_csv(nombre, index=False)


# for bacteria in df_biomasas:
#     select_column = df_biomasas[['cycle', 'Score']]

# for label, values in df_biomasas_final.items():
#     biomasas = values
#     id = values
#     cycles_final = df_cycles

#     try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
#         df = pd.DataFrame()
#         print(df)
#         df.to_csv('04_resultados/rizo/biomasas/bacillus_data.csv', index=False)




# final_biomass = final_models['Bacillus']
# cycles = final_models['cycle']


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
# df = pd.DataFrame(final_models, columns=['cycle', 'Bacillus'])
# print(df)
# df.to_csv('04_resultados/rizo/biomasas/bacillus_data.csv', index=False)

# print(f"ÉXITO: {model_id} registrado y guardado en {csv_file_name}")
# print("========================================================")
# print(f"TABLA DE CRECIMIENTO: {model_id}")
# print("========================================================")
# print(final_models.to_string())

