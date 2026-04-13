# https://cometspy.readthedocs.io/en/latest/getting_started.html#preparing-a-model-for-comets
from cobra.io import load_model
import cometspy as c

# Load a textbook example model using the COBRAPy toolbox 
test_model = load_model('textbook')

# Use the above model to create a COMETS model
test_model = c.model(test_model)

# Change comets specific parameters, e.g. the initial biomass of the model
# Notre 
test_model.initial_pop = [0, 0, 1e-7] 


my_layout = c.layout(test_model)

my_layout.media

my_simulation = c.comets(my_layout, my_params)
my_simulation.run()