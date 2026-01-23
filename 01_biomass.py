import cometspy as c
import cobra.io
import pandas as pd
import os
import glob
from biomass_funtion import biomass_comunidades_rizo



biomass_comunidades_rizo(
    ruta_csv_syncoms='./02_data/rizo/syncom.csv',
    patron_xml='./02_data/rizo/carveme/ST*_prokka_carveme_lb.xml', 
    folder_resultados='./04_resultados/rizo/biomasas/comunidades')