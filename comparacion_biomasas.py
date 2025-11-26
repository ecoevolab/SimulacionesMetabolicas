import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np 
import os 
import matplotlib.cm as cm 
import math
# ----------------------------------------------------
# Crear variables
# Directorio donde se encuentran todos los CSV de biomasa
BASE_PATH = '01_data/rizo/carveme' 
# Encontrar todos los archivos CSV de biomasa

csv_files = ('04_resultados/rizo/biomasas/ST00046_prokka_carveme_lb.csv', 
              '04_resultados/rizo/biomasas/bacillus_data.csv')

df1 = pd.read_csv('./04_resultados/rizo/biomasas/ST00046_prokka_carveme_lb.csv')
df2 = pd.read_csv('./04_resultados/rizo/biomasas/bacillus_data.csv')

masa = df1.iloc[:, 1]
log_masa = np.log10(masa + 1e-10)

masa2 = df2.iloc[:, 1]
log_masa2 = np.log10(masa2 + 1e-10)


# Plot the first dataset
plt.plot(df1['cycle'], np.log(df1['ST00046'] + 1e-10), color='#1A3749', label='sola', marker='o')

# Plot the second dataset on the *same* figure
plt.plot(df2['cycle'], np.log(df2['ST00046'] + 1e-10), color='#1A3749', label='comunidad', linestyle='--')

# Add labels, title, and a legend for clarity
plt.xlabel('X-axis values')
plt.ylabel('Y-axis values')
plt.title('Comparacion en el crecimiento')
plt.legend() # This is crucial for differentiating the datasets

# Display the plot
plt.show()
