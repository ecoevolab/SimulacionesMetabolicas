# ==========================================================
# VARIABLES DE ENTORNO (ANTES DE IMPORTAR COMETSPY)
# ==========================================================
import os

GUROBI_PATH = "/opt/gurobi1201/linux64"

os.environ["GUROBI_HOME"] = GUROBI_PATH
os.environ["GUROBI_COMETS_HOME"] = GUROBI_PATH
os.environ["LD_LIBRARY_PATH"] = f"{GUROBI_PATH}/lib"

print("GUROBI_HOME:", os.environ.get("GUROBI_HOME"))

# ==========================================================
# IMPORTS
# ==========================================================
import cometspy as c
import cobra.io
import pandas as pd
from matplotlib import pyplot as plt

# ==========================================================
# WORKING DIRECTORY
# ==========================================================
working_dir = "./comets_runs"
os.makedirs(working_dir, exist_ok=True)

# ==========================================================
# CREATE LAYOUT
# ==========================================================
test_tube = c.layout()

# Media conditions
test_tube.set_specific_metabolite('glc__D_e', 0.011)  # 11 mM glucose
test_tube.set_specific_metabolite('o2_e', 0)

test_tube.set_specific_metabolite('nh4_e', 1000)
test_tube.set_specific_metabolite('pi_e', 1000)
test_tube.set_specific_metabolite('h2o_e', 1000)
test_tube.set_specific_metabolite('h_e', 1000)

# ==========================================================
# LOAD MODEL
# ==========================================================
cobra_model = cobra.io.read_sbml_model(
    './02_data/rizo/carveme/ST00101_prokka_carveme_lb.xml'
)

ST00101 = c.model(cobra_model)
ST00101.id = 'ST00101'

# Exchange bounds
ST00101.change_bounds('EX_glc__D_e', -1000, 1000)

# Initial biomass
ST00101.initial_pop = [0, 0, 5e-6]

# Add to layout
test_tube.add_model(ST00101)

# ==========================================================
# SIMULATION PARAMETERS
# ==========================================================
sim_params = c.params()
sim_params.working_dir = working_dir
sim_params.max_cycles = 100

experiment = c.comets(test_tube, sim_params)

# ==========================================================
# RUN SIMULATION (CON DEBUG)
# ==========================================================
try:
    print("Running COMETS simulation ...")
    experiment.run()
    print("✅ Simulation completed successfully")

except RuntimeError as e:
    print("\n❌ ERROR EN COMETS")
    print(e)
    print("\n==== JAVA TRACE ====")
    print(experiment.run_output)
    raise

# ==========================================================
# PLOTS
# ==========================================================
# Biomass
ax = experiment.total_biomass.plot(x='cycle')
ax.set_ylabel("Biomass (g)")
plt.show()

# Media time series
media = experiment.media.copy()
media = media[media.conc_mmol < 900]

fig, ax = plt.subplots()

for met in media.metabolite.unique():
    subset = media[media.metabolite == met]
    subset.plot(x='cycle', y='conc_mmol', ax=ax)

ax.set_ylabel("Concentration (mmol)")
plt.show()
#############################################
import cometspy as c
import cobra.io
import os
import pandas as pd

# Load the model
STECOLI = c.model(cobra.io.read_sbml_model('./02_data/rizo/carveme/STECOLI_prokka_carveme_lb.xml'))
STECOLI.id = 'Ecoli'

# Set initial population: [x, y, biomass_in_grams]
STECOLI.initial_pop = [0, 0, 5e-8]

# Create layout and add model
test_tube = c.layout()
test_tube.add_model(STECOLI)
dilution_rate = 0.1
# --- FIX: Loop through your metabolite dictionary ---
metabolites = {
    "h2o_e": 100*dilution_rate, "o2_e": 10, "pi_e": 10, "prbamp_e": 10, "zn2_e": 10, 
    "cobalt2_e": 10, "k_e": 10, "mg2_e": 10, "na1_e": 10, "cd2_e": 10, 
    "aso4_e": 10, "fe2_e": 10, "fe3_e": 10, "cro4_e": 10, "nh3_c": 10, 
    "pheme": 10, "cmp": 10, "ump": 10, "gmp": 10, "pydx": 10, "nac": 10, 
    "ribflv": 10, "pphn": 10, "hxan": 10, "glu__L_e": 0.1*dilution_rate, "gly_e": 0.1*dilution_rate,
    "ala__L_e": 0.1*dilution_rate, "lys__L_e": 0.1*dilution_rate, "asp__L_e": 0.1*dilution_rate,
    "so4_e": 0.1*dilution_rate,
    "arg__L_e": 0.1*dilution_rate, "ser__L_e": 0.1*dilution_rate, "cu2_e": 0.1*dilution_rate, "met__L_e": 0.1*dilution_rate, 
    "trp__L_e": 0.1*dilution_rate, "phe__L_e": 0.1*dilution_rate, "h_e": 0.1*dilution_rate, "tyr__L_e": 0.1*dilution_rate, 
    "cys__L_e": 0.1*dilution_rate, "ura_e": 0.1*dilution_rate, "cl_e": 0.1*dilution_rate, "leu__L_e": 0.1*dilution_rate, 
    "his__L_e": 0.1*dilution_rate, "pro__L_e": 0.1*dilution_rate, "val__L_e": 0.1*dilution_rate, "thr__L_e": 0.1*dilution_rate, "ile__L_e": 0.1*dilution_rate 
}

for met, conc in metabolites.items():
    test_tube.set_specific_metabolite(met, conc)

# Add trace metabolites as static (infinite supply)
trace_metabolites = ['ca2_e', 'cl_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e', 'h_e', 'k_e', 'h2o_e', 'mg2_e',
                     'mn2_e', 'mobd_e', 'na1_e', 'ni2_e', 'nh4_e', 'o2_e', 'pi_e', 'so4_e', 'zn2_e']

for i in trace_metabolites:
    test_tube.set_specific_metabolite(i, 1000)
    test_tube.set_specific_static(i, 1000)

# Parameters setup
comp_params = c.params()
comp_params.set_param('timeStep', 0.1)
comp_params.set_param('maxCycles', 80)
# To see all params in a notebook: print(comp_params.all_params)

# Run simulation
comp_assay = c.comets(test_tube, comp_params)
comp_assay.run()

########################

media = comp_assay.media.copy()
media = media[media.conc_mmol<900]







