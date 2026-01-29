import cometspy as c
import cobra.io
import os
from function_biomass import biomass_comunidades_rizo

# --- CONFIGURACIÓN DEL MEDIO LB ---
dilution_rate = 0.1
# Nota: Se eliminó nh3_c y pheme porque COMETS requiere metabolitos extracelulares (_e)
lb = {
    "h2o_e": 100*dilution_rate, "o2_e": 10, "pi_e": 10, "zn2_e": 10, 
    "cobalt2_e": 10, "k_e": 10, "mg2_e": 10, "na1_e": 10, "cd2_e": 10, 
    "aso4_e": 10, "fe2_e": 10, "fe3_e": 10, "cro4_e": 10, 
    "pydx_e": 10, "nac_e": 10, "ribflv_e": 10, "ura_e": 0.1*dilution_rate,
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
    ruta_csv_syncoms='/mnt/data/sur/users/mmontante/02_data/rizo/syncom_indiv.csv',
    patron_xml='/mnt/data/sur/users/mmontante/02_data/rizo/carveme/ST*_prokka_carveme_lb.xml',
    threads=4,      # Ajusta según tu CPU
    cycles=480,      # Número de pasos de tiempo
    mass=5e-8,      # Masa inicial por bacteria
    media=lb,       # Diccionario definido arriba
    folder_resultados='/mnt/data/sur/users/mmontante//04_results/rizo/biomass_indiv/'
)






