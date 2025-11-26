# import pandas as pd
# import matplotlib.pyplot as plt
# import glob
# import numpy as np 
# import os 
# import matplotlib.cm as cm 
# import math
# # ----------------------------------------------------
# # Crear variables
# # Directorio donde se encuentran todos los CSV de biomasa
# BASE_PATH = '01_data/rizo/carveme' 
# # Encontrar todos los archivos CSV de biomasa

# csv_files = ('04_resultados/rizo/biomasas/ST00046_prokka_carveme_lb.csv', 
#               '04_resultados/rizo/biomasas/bacillus_data.csv')
# path = './04_resultados/rizo/biomasas/'
# all_files = glob.glob(os.path.join(path, "*_bueno.csv")) 
# df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# # df1 = pd.read_csv('./04_resultados/rizo/biomasas/ST00046_prokka_carveme_lb.csv')
# # df2 = pd.read_csv('./04_resultados/rizo/biomasas/bacillus_data.csv')


# for i in df:
#     plt.plot(i['cycle'], np.log(i.iloc[:, 1] + 1e-10), color='#1A3749', label='sola', marker='o')
#     plt.xlabel('X-axis values')
#     plt.ylabel('Y-axis values')
#     plt.title('Comparacion en el crecimiento')
#     plt.legend() # This is crucial for differentiating the datasets

# # Display the plot
#     plt.show()




# # masa2 = df2.iloc[:, 1]
# # log_masa2 = np.log10(masa2 + 1e-10)


# # Plot the first dataset
# # plt.plot(df1['cycle'], np.log(df1['ST00046'] + 1e-10), color='#1A3749', label='sola', marker='o')

# # Plot the second dataset on the *same* figure
# # plt.plot(df2['cycle'], np.log(df2['ST00046'] + 1e-10), color='#1A3749', label='comunidad', linestyle='--')

# # Add labels, title, and a legend for clarity
# # plt.xlabel('X-axis values')
# # plt.ylabel('Y-axis values')
# # plt.title('Comparacion en el crecimiento')
# # plt.legend() # This is crucial for differentiating the datasets

# # # Display the plot
# # plt.show()


# import pandas as pd
# import matplotlib.pyplot as plt
# import glob
# import numpy as np 
# import os 

# path = './04_resultados/rizo/biomasas/'
# all_files = glob.glob(os.path.join(path, "*_bueno.csv"))
# all_file = glob.glob(os.path.join(path, "*_dimont_carveme_lb.csv"))


# for file in all_files:
#     df = pd.read_csv(file)

#     # Segunda columna = biomasa
#     masa = df.iloc[:, 1]

#     # Nombre bonito para el título
#     nombre = os.path.basename(file).replace('_bueno.csv','')
#     for files in all_file:
#         dfs = pd.read_csv(files)
#         masa = dfs.iloc[:, 1]

#     # Gráfica individual
#     plt.plot(df['cycle'], np.log(df['ST00046'] + 1e-10), color='#1A3749', label='sola', marker='o')
#     plt.plot(dfs['cycle'], np.log(dfs['ST00046'] + 1e-10), color='#1A3749', label='comunidad', linestyle= '--')
#     plt.xlabel('Cycle')
#     plt.ylabel('Log Biomasa')
#     plt.title(f'Crecimiento de {nombre}')
#     plt.grid(True)
#     plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np 
import os 

path = './04_resultados/rizo/biomasas/'

# Archivos individuales
all_files = glob.glob(os.path.join(path, "*_bueno.csv"))

# Archivo de comunidad (asumo solo 1)
comunidad_file = glob.glob(os.path.join(path, "*_dimont_carveme_lb.csv"))[0]
df_com = pd.read_csv(comunidad_file)

# Segunda columna del archivo de comunidad
col_com = df_com.columns[1]
colores = ['#80B6B3', '#3D788E', '#5F9EAD', '#1A3749', '#26526B']

for i, file in enumerate(all_files):
    df = pd.read_csv(file)

    col_ind = df.columns[1]
    nombre = os.path.basename(file).replace('_bueno.csv','')

    plt.plot(df['cycle'], np.log(df[col_ind] + 1e-10),
             color= colores[i % len(colores)],
             label='sola', marker='o')

    plt.plot(df_com['cycle'], np.log(df_com[col_com] + 1e-10),
             color= colores[i % len(colores)],
             label='comunidad', linestyle='--')

    plt.xlabel('Cycle')
    plt.ylabel('Log Biomasa')
    plt.title(f'Crecimiento de {nombre}')
    plt.grid(True)
    plt.legend()
    plt.show()
