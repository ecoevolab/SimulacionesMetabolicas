# https://cometspy.readthedocs.io/en/latest/getting_started.html#preparing-a-model-for-comets
import cobra
from cobra.io import load_model
import cometspy as c

# Load a textbook example model using the COBRAPy toolbox 
test_model = load_model('textbook')

# Use the above model to create a COMETS model
test_model = c.model(test_model)

# Change comets specific parameters, e.g. the initial biomass of the model
# Notre 
test_model.initial_pop = [0, 0, 1e-7] 



# Create a parameters object with default values 
my_params = c.params()

# Change the value of a parameter, for example number of simulation cycles
my_params.set_param('maxCycles', 100)

# Set some writeTotalBiomassLog parameter to True, in order to save the output
my_params.set_param('writeTotalBiomassLog', True)

# See avaliable parameters and their values
my_params.show_params()




my_layout = c.layout(test_model)

my_layout.media

my_simulation = c.comets(my_layout, my_params)
my_simulation.run()