import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import csv

model_path = '02_data/rizo/carveme/ST*_prokka_carveme_lb.xml'
cobra_models = c.model(cobra.io.read_sbml_model(model_path))

test_tube = c.layout()
initial_mass = [0, 0, 5e-8]   
