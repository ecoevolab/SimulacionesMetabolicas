from cometsassay import comets

# --- CONFIGURACIÓN DEL MEDIO LB ---
dilution_rate = 0.1
# Nota: Se eliminó nh3_c y pheme porque COMETS requiere metabolitos extracelulares (_e)
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
comets(
ruta_csv_syncoms= '/mnt/data/sur/users/mmontante/02_data/rizo/syncoms_indiv.csv',
patron_xml= '/mnt/data/sur/users/mmontante/02_data/rizo/carveme/ST*_prokka_carveme_lb.xml',
threads= 1,     
cycles= 10,     
mass= 5e-8,      
media= lb,       
folder_temp= '/mnt/data/sur/users/mmontante/04_resultados/rizo/temporal/',
folder_results= '/mnt/data/sur/users/mmontante/04_resultados/rizo/resultados'
)

