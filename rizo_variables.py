import cometspy as c
import cobra.io
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np 
import csv

csv_output_path = '04_resultados/rizo/reacciones'

all_models = {} 
all_model = {}
model_summary = {}
model_reactions = {} 
model_metabolites = {}
model_genes = {}

paths = {
    "prokka": glob.glob('./02_data/rizo/carveme/ST*_prokka_carveme_lb.xml'),
    "eggnog": glob.glob('./02_data/rizo/carveme/ST*_eggnog_carveme_lb.xml'),
    "dimont": glob.glob('./02_data/rizo/carveme/ST*_dimont_carveme_lb.xml')
}


for anotacion in paths:
    for model_path in anotacion:
         #1. Extraction and setup
        file_name = os.path.basename(model_path)
        model_id = file_name.replace('.xml', '') 
    
    if '-draft' in file_name:
        continue 
    
    try: 
        # 2. Loading and processing
        cobra_models = cobra.io.read_sbml_model(model_path)
        #all_model[model_id] = cobra_models
        #processed_models = c.model(cobra_models) 

        # 3. Store data (CORRECCIÓN CLAVE EN ESTE BLOQUE)
        
        # Guardar el objeto modelo completo
        all_models[model_id] = cobra_models 
        
        # Guardar el conteo de reacciones en una VARIABLE TEMPORAL
        number_of_reactions = len(cobra_models.reactions)
        number_of_metabolites = len(cobra_models.metabolites)
        number_of_genes = len(cobra_models.genes)

                # Registrar el conteo en el DICCIONARIO model_reactions
        model_reactions[model_id] = number_of_reactions 
        model_metabolites[model_id] = number_of_metabolites
        model_genes[model_id] = number_of_genes
        print(f"Modelo {model_id} cargado. Total de reacciones: {number_of_reactions}")
        print(f"Modelo {model_id} cargado. Total de reacciones: {number_of_metabolites}")
        print(f"Modelo {model_id} cargado. Total de reacciones: {number_of_genes}")



        # ... (el resto del código de simulación) ...
        
    except Exception as e:
        print(f"ERROR: Failed to process model {model_id} from {file_name}. Error: {e}")


