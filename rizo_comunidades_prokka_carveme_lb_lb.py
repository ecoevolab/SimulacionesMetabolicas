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



#ruta_C2R = '/home/abigaylmontantearenas/Documents/practicas/MODELOS/data/GEM/cvm_C2R.xml'
#ruta_RC3 = '/home/abigaylmontantearenas/Documents/practicas/MODELOS/data/GEM/cvm_RC3.xml'


ST42 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00042_prokka_carveme_lb.xml'))
ST42.id = 'Pumsongensis'
ST46 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00046_prokka_carveme_lb.xml'))
ST46.id = 'Bacillus'
ST101 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00101_prokka_carveme_lb.xml'))
ST101.id = 'Pseudomonas'
ST109 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00109_prokka_carveme_lb.xml'))
ST109.id = 'Mycobacterium'
ST154 = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/ST00154_prokka_carveme_lb.xml'))
ST154.id = 'Agrobacterium'

# set its initial biomass, 5e-6 gr at coordinate [0,0]
ST42.initial_pop = [0, 0, 5e-8]
ST46.initial_pop = [0, 0, 5e-8]
ST101.initial_pop = [0, 0, 5e-8]
ST109.initial_pop = [0, 0, 5e-8]
ST154.initial_pop = [0, 0, 5e-8]

# create an empty layout
test_tube = c.layout()

# add the models to the test tube
test_tube.add_model(ST42)
test_tube.add_model(ST46)
test_tube.add_model(ST101)
test_tube.add_model(ST109)
test_tube.add_model(ST154)

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



strains = [
    r'$\it{Pseudomonas\ umsongensis}$ (ST00042)',   
    r'$\it{Bacillus\ spp.}$ (ST00046)', 
    r'$\it{Pseudomonas\ spp.}$ (ST00101)', 
    r'$\it{Mycobacterium\ spp.}$ (ST00109)', 
    r'$\it{Agrobacterium\ sp.}$ (ST00154)'    
]
pallete = ('#80B6B3','#1A3749','#5F9EAD','#3D788E','#26526B')

plt.figure(figsize=(20, 8))
biomass = comp_assay.total_biomass
log_biomass = np.log10(biomass + 1e-10)
log_biomass['t'] = biomass['cycle'] * comp_assay.parameters.all_params['timeStep']
t = biomass['cycle'] * comp_assay.parameters.all_params['timeStep']


# df = pd.DataFrame({
#     'time': t,
#     'biomasa': biomass,
#     'log_biomass': log_biomass
# })

# print(df)

# 2. PLOTEAR: Dibuja todas las curvas vs. 't', asignando los 5 colores Hex
myplot = log_biomass.drop(columns=['cycle']).plot(
    x = 't', 
    linewidth=5, 
    color=pallete # Aplica la lista de 5 colores a las 5 curvas
)

# 3. CORREGIR ETIQUETAS (para usar los nombres científicos)
# Usa zip para mapear cada línea dibujada a su etiqueta científica correspondiente
for line, new_label in zip(myplot.get_lines(), strains):
    line.set_label(new_label)

# 4. CONFIGURACIÓN DE EJES Y LEYENDA
myplot.set_ylabel(r'biomass [$\it{log10}$($\bf{g}$)]', fontsize=12)
plt.xlabel('time (h)', fontsize=12) 
#plt.title('Curvas de Crecimiento Microbiano', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

# Ajuste de Leyenda (Ubicación y Fuente)
plt.legend(title='Strain ID', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8) 

# Ajuste el layout para que la leyenda y las etiquetas no se corten
plt.tight_layout() 

# 5. GUARDAR Y MOSTRAR
output_folder = '04_resultados/rizo/graficas'
output_path = os.path.join(output_folder, 'competencia80_log10_1_2511.png')
os.makedirs(output_folder, exist_ok=True) # Asegurar directorio

plt.savefig(output_path, bbox_inches='tight') # Usa tight para guardar bien la leyenda
plt.show()





