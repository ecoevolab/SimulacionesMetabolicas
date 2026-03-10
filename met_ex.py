import cometspy as c
import cobra.io
import os
import pandas as pd
from matplotlib import pyplot as plt


E_no_galE = cobra.test.create_test_model("ecoli")
E_no_LCTStex = E_no_galE.copy()
E_no_galE.genes.b0759.knock_out()

E_no_LCTStex.reactions.LCTStex.knock_out() 

E_no_galE.id = "galE_KO" 
E_no_LCTStex.id = "LCTStex_KO" 
galE_comets = c.model(E_no_galE) 
lcts_comets = c.model(E_no_LCTStex)