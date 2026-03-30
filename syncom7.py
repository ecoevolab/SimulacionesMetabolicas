import cometspy as c
import cobra.io
import os
from biomass_funtion import biomass_comunidades_rizo

# --- CONFIGURACIÓN DEL MEDIO LB ---
dilution_rate = 0.1

lb = {
    "h2o_e": 100*dilution_rate, "o2_e": 10*dilution_rate, "pi_e": 10*dilution_rate, "zn2_e": 10, 
    "cobalt2_e": 10*dilution_rate, "k_e": 10*dilution_rate, "mg2_e": 10*dilution_rate, "na1_e": 10*dilution_rate, "cd2_e": 10*dilution_rate, 
    "aso4_e": 10*dilution_rate, "fe2_e": 10*dilution_rate, "fe3_e": 10*dilution_rate, "cro4_e": 10*dilution_rate, 
    "pydx_e": 10*dilution_rate, "nac_e": 10*dilution_rate, "ribflv_e": 10*dilution_rate, "ura_e": 0.1*dilution_rate,
    "glu__L_e": 0.1*dilution_rate, "gly_e": 0.1*dilution_rate,
    "ala__L_e": 0.1*dilution_rate, "lys__L_e": 0.1*dilution_rate, 
    "asp__L_e": 0.1*dilution_rate, "so4_e": 0.1*dilution_rate,
    "arg__L_e": 0.1*dilution_rate, "ser__L_e": 0.1*dilution_rate, 
    "cu2_e": 0.1*dilution_rate, "met__L_e": 0.1*dilution_rate, 
    "trp__L_e": 0.1*dilution_rate, "phe__L_e": 0.1*dilution_rate, 
    "h_e": 0.1*dilution_rate, "tyr__L_e": 0.1*dilution_rate, 
    "cys__L_e": 0.1*dilution_rate, "cl_e": 0.1*dilution_rate, 
    "leu__L_e": 0.1*dilution_rate, "his__L_e": 0.1*dilution_rate, 
    "pro__L_e": 0.1*dilution_rate, "val__L_e": 0.1*dilution_rate, 
    "thr__L_e": 0.1*dilution_rate, "ile__L_e": 0.1*dilution_rate
}

# --- EJECUCIÓN ---
biomass_comunidades_rizo(
    ruta_csv_syncoms='/mnt/data/sur/users/mmontante/02_data/rizo/syncom7.csv',
    patron_xml='/mnt/data/sur/users/mmontante/02_data/rizo/carveme/ST*_prokka_carveme_lb.xml',
    threads=8,      # Ajusta según tu CPU
    cycles=160,      # Número de pasos de tiempo
    mass=5e-8,      # Masa inicial por bacteria
    media=lb,       # Diccionario definido arriba
    folder_resultados='/mnt/data/sur/users/mmontante/04_resultados/rizo/syncom7'
)


