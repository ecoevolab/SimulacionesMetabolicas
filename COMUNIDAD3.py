import cometspy as c
import cobra.io
import cometspy as c 
from matplotlib import pyplot as plt 
import pandas as pd

# Load the E. coli iJO1366 model 
E_no_galE = cobra.test.create_test_model("ecoli") 
# copy it 
E_no_LCTStex = E_no_galE.copy() 
# Perform galE KO in the first model 
E_no_galE.genes.b0759.knock_out() # cannot metabolize galactose 
# Perform LCTStex reaction KO in the second model 
E_no_LCTStex.reactions.LCTStex.knock_out() # cannot uptake lactose


# change the ids of the models 
E_no_galE.id = "galE_KO" 
E_no_LCTStex.id = "LCTStex_KO" 
# make COMETS models from the cobrapy models 
galE_comets = c.model(E_no_galE) 
lcts_comets = c.model(E_no_LCTStex)

initial_pop = 1.e-3 # gDW 
galE_comets.initial_pop = [0,0,initial_pop] # x, y, gDW 
lcts_comets.initial_pop = [0,0,initial_pop] # x, y, gDW
galE_comets.open_exchanges() 
lcts_comets.open_exchanges()

galE_comets.obj_style = "MAX_OBJECTIVE_MIN_TOTAL" # default FBA option is "MAXIMIZE_OBJECTIVE_FLUX" 
lcts_comets.obj_style = "MAX_OBJECTIVE_MIN_TOTAL"

layout = c.layout([galE_comets, lcts_comets])
unlimited_mets = ['ca2_e', 'cl_e', 'co2_e', 'cobalt2_e', 'cu2_e', 'fe2_e', 'fe3_e','h_e', 'h2o_e', 'k_e', 'mg2_e', 'mn2_e', 'mobd_e', 'na1_e', 'nh4_e', 'ni2_e','o2_e', 'pi_e', 'sel_e', 'slnt_e', 'so4_e', 'tungs_e', 'zn2_e']  
for met in unlimited_mets: 
    layout.set_specific_metabolite(met, 1000.) 
    layout.set_specific_metabolite("lcts_e", 1.)

dilution_rate = 0.1 # / hr for met in unlimited_mets: 
layout.set_specific_refresh(met, 1000. * dilution_rate) # 100 mmol / hour 
layout.set_specific_refresh("lcts_e", 1. * dilution_rate) # 0.1 mmol / hour

params = c.params()

params.set_param("deathRate", dilution_rate) 
params.set_param("metaboliteDilutionRate", dilution_rate)

params.set_param("spaceWidth", 0.1) 
params.set_param("defaultVmax", 15.) 
params.set_param("defaultKm", 0.0001)

params.set_param("timeStep", 0.1) # hours 
params.set_param("maxSpaceBiomass", 10.) 
params.set_param("maxCycles", 300)

params.set_param(“writeFluxLog”, True) 
params.set_param(“writeMediaLog”, True) 
params.set_param(“FluxLogRate”, 1) 
params.set_param(“MediaLogRate”, 1)