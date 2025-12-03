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

path = './04_resultados/rizo/biomasas/bioss/ensayo'
output_path = './04_resultados'

# Buscar archivos
com_files = glob.glob(os.path.join(path, "*_bueno.csv"))
comunidad_files = glob.glob(os.path.join(path, "*_prokka_carveme_lb_80.csv"))

# Crear diccionarios usando el nombre base
com_dict = {
    os.path.basename(f).replace("_bueno.csv", ""): f
    for f in com_files
}

indi_dict = {
    os.path.basename(f).replace("_prokka_carveme_lb_80.csv", ""): f
    for f in comunidad_files
}

colores = ['#26526B', '#1A3749', '#3D788E', '#5F9EAD', '#80B6B3']

# Encontrar nombres que EXISTEN en ambos
nombres_comunes = set(com_dict.keys()) & set(indi_dict.keys())

for i, nombre in enumerate(sorted(nombres_comunes)):

    # Leer ambos archivos del par
    df_coms = pd.read_csv(com_dict[nombre])
    df_indis = pd.read_csv(indi_dict[nombre])
    
    y_com = df_coms.iloc[:, 0] * 0.1
    y_ind = df_indis.iloc[:, 0] * 0.1

    col_ind = df_coms.columns[1]
    col_com = df_indis.columns[1]

    # Graficar Individual
    plt.plot(df_coms.iloc[:, 0] * 0.1, np.log(df_coms[col_ind] + 1e-10),
             color= colores[i % len(colores)],
             label='comunidad', marker='o')


    # Graficar Comunidad
    plt.plot(df_coms.iloc[:, 0] * 0.1, np.log(df_indis[col_com] + 1e-10),
             color= colores[i % len(colores)],
             label='individual', linestyle='--')

    plt.xlabel('t(h)')
    plt.ylabel((r'Biomasa [$\it{log10}$($\bf{g}$)]'))
    plt.title(f'Crecimiento de {nombre}')
    plt.grid(True)
    plt.legend()
    
    # Crear nombre del archivo
    filename = f"comparacion_biomasas_{nombre}.png"
    filepath = os.path.join(output_path, filename)

    # Guardar ANTES del show
    plt.savefig(filepath, dpi=300, bbox_inches='tight')

    # Mostrar
    plt.show()

    # Limpiar figura para la siguiente
    plt.clf()


