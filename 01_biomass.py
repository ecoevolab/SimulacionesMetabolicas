# -------------------------------------------
# Genoma anotado en dimont, prokka o eggnog y GEM recostruido en carveme
# ---------------------------------------------
# Cargar paqutes 
import cometspy as c
import cobra.io
import pandas as pd #libreria para manejar tablas
import os # crear carpetas y ''extraer'' nombres 
import glob # para seleccionar varios archivos
from biomass_funtion import biomass_rizo 
# --------------------------
# Cargar variables, rutas y parametros
# Diccionarios para almacenar datos mas adelante
# Parametors de la simulación
# en vez de glob glob podría usar: 
# import os

# for dirpath, dirnames, filenames in os.walk('.'):
#     for filename in filenames:
#         if filename.endswith('.txt'):
#             full_path = os.path.join(dirpath, filename)
#             print(full_path)

# dimont_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_dimont_carveme_lb.xml'))
# eggnoge_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_eggnog_carveme_lb.xml'))
# prokka_carve = sorted(glob.glob('02_data/rizo/carveme/ST*_prokka_carveme_lb.xml'))

# model_paths = [dimont_carve, eggnoge_carve, prokka_carve]

# biomass_rizo(dimont_carve, 0, 0, 5e-8, 80)

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/syncoms.csv')

# Display the first few rows of the DataFrame

import csv

import csv

with open('/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data/rizo/syncoms.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)




# comunidad = list(zip(id, value))

# print(comunidad)
# selected_models = []

# prokka_carve = glob.glob('02_data/rizo/carveme/ST*_prokka_carveme_lb.xml')

# for strain, val in comunidad:
#     if val == 1:
#         for model in prokka_carve:
#             if strain in os.path.basename(model):
#                 selected_models.append(model)
            
# print(selected_models)            
