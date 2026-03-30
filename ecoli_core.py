import cometspy as c
import cobra.io
import os
import pandas as pd

# --- 1. Configuración de Rutas ---
output_path = '/mnt/data/sur/users/mmontante/04_resultados/rizo/'

# Crear el directorio si no existe
if not os.path.exists(output_path):
    os.makedirs(output_path)

# --- 2. Carga del Modelo y Layout ---
STECOLI = c.model(cobra.io.read_sbml_model('/mnt/data/sur/users/mmontante/02_data/rizo/carveme/ST0101_prokka_carveme_lb.xml'))
STECOLI.id = 'Ecoli'
STECOLI.initial_pop = [0, 0, 5e-8]

test_tube = c.layout()
test_tube.add_model(STECOLI)
dilution_rate = 0.1

metabolites = {
    "h2o_e": 10, "o2_e": 10, "pi_e": 10, "prbamp_e": 10, "zn2_e": 10, 
    "cobalt2_e": 10, "k_e": 10, "mg2_e": 10, "na1_e": 10, "cd2_e": 10, 
    "aso4_e": 10, "fe2_e": 10, "fe3_e": 10, "cro4_e": 10, "nh3_c": 10, 
    "pheme": 10, "cmp": 10, "ump": 10, "gmp": 10, "pydx": 10, "nac": 10, 
    "ribflv": 10, "pphn": 10, "hxan": 10, "glu__L_e": 0.01, "gly_e": 0.01,
    "ala__L_e": 0.01, "lys__L_e": 0.01, "asp__L_e": 0.01, "so4_e": 0.01,
    "arg__L_e": 0.01, "ser__L_e": 0.01, "cu2_e": 0.01, "met__L_e": 0.01, 
    "trp__L_e": 0.01, "phe__L_e": 0.01, "h_e": 0.01, "tyr__L_e": 0.01, 
    "cys__L_e": 0.01, "ura_e": 0.01, "cl_e": 0.01, "leu__L_e": 0.01, 
    "his__L_e": 0.01, "pro__L_e": 0.01, "val__L_e": 0.01, "thr__L_e": 0.01, "ile__L_e": 0.01 
}

for met, conc in metabolites.items():
    test_tube.set_specific_metabolite(met, conc)

trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 'k_e', 'h2o_e', 'mg2_e',
                     'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

for i in trace_metabolites:
    test_tube.set_specific_metabolite(i, 1000)
    test_tube.set_specific_static(i, 1000)

# --- 3. Parámetros y Activación de Logs ---
comp_params = c.params()
comp_params.set_param('timeStep', 0.1)
comp_params.set_param('maxCycles', 80)
comp_params.set_param('writeMediaLog', True)
comp_params.set_param('MediaLogRate', 1)
comp_params.set_param('writeTotalBiomassLog', True)

# --- 4. Ejecución ---
comp_assay = c.comets(test_tube, comp_params)
comp_assay.run()

# --- 5. Procesamiento y Guardado de Resultados ---

# A. Guardar Serie de Tiempo de Metabolitos (Formato Limpio/Pivoteado)
# Usamos un umbral de 500 para excluir los trace_metabolites estáticos (que valen 1000)
df_metabolites = comp_assay.get_metabolite_time_series(upper_threshold=500.0)
df_metabolites.to_csv(os.path.join(output_path, 'serie_tiempo_metabolitos.csv'), index=False)

# B. Guardar Biomasa Total
df_biomasa = comp_assay.total_biomass
df_biomasa.to_csv(os.path.join(output_path, 'crecimiento_biomasa.csv'), index=False)

# C. Guardar solo los Metabolitos Finales (Último ciclo)
ultimo_ciclo = df_metabolites['cycle'].max()
metabolitos_finales = df_metabolites[df_metabolites['cycle'] == ultimo_ciclo]
metabolitos_finales.to_csv(os.path.join(output_path, 'concentraciones_finales.csv'), index=False)

print(f"Archivos guardados exitosamente en: {output_path}")
