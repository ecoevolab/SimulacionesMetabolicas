# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import tkinter as tk

# # df1 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_dimont_carveme_lb_1.csv')
# # df2 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_prokka_carveme_lb.csv')

# # df2.loc[1, 'ST00094_prokka_carveme_lb'] = 'ST00094'
# # df2.loc[2, 'ST00101_prokka_carveme_lb'] = 'ST00101'
# # df2.loc[3, 'ST00000_prokka_carveme_lb'] = 'ST00000'
# # df2.loc[4, 'ST00109_prokka_carveme_lb'] = 'ST00109'
# # df2.loc[5, 'ST00060_prokka_carveme_lb'] = 'ST00060'
# # df2.loc[6, 'ST00046_prokka_carveme_lb'] = 'ST00046'

# # df1_reacs = pd.DataFrame(df1)
# # df2_reacs = pd.DataFrame(df2)

# # model_ids = df2['Model ID']

# # total_reactions1 = df1_reacs['Total Reactions']
# # print(len(total_reactions1))

# # total_reactions2 = df2_reacs['Total Reactions']
# # print(len(total_reactions2))

# # # bar_width = 0.35 
# # # r_reactions1 = np.arange(len(model_ids)) # Posiciones para Reacciones
# # # r_reactions2 = [x + bar_width for x in r_reactions1] # Posicifileón DESPLAZADA para Metabolitos


# # # plt.figure(figsize=(12, 6))

# # # # 1. Plotear la primera serie (Reacciones)
# # # plt.bar(r_reactions1, total_reactions1, 
# # #         color='#1F77B4', 
# # #         width=bar_width, 
# # #         label='Total de Reacciones')

# # # # 2. Plotear la segunda serie (Metabolitos)
# # # plt.bar(r_reactions2, total_reactions2, 
# # #         color='#FF7F0E', 
# # #         width=bar_width, 
# # #         label='Total de Metabolitos')


# # # # --- 5. CONFIGURACIÓN FINAL ---


# # # plt.xlabel('Model ID', fontsize=12)
# # # plt.ylabel('Conteo', fontsize=12)
# # # plt.title('Comparación Agrupada: Tamaño de la Red Metabólica', fontsize=14)

# # # # Definir las etiquetas del eje X en las posiciones centrales
# # # plt.xticks([r + bar_width / 2 for r in r_reactions1], model_ids, rotation=45, ha='right', fontsize=10)

# # # plt.legend(loc='upper left')
# # # plt.tight_layout()
# # # plt.show()



# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import os

# df1 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_dimont_carveme_lb_4.csv')
# df2 = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_prokka_carveme_lb_4.csv')

# df1_reacs = pd.DataFrame(df1)
# df2_reacs = pd.DataFrame(df2)

# model_ids = df1_reacs['Model ID']
# print(model_ids)

# total_reactions1 = df1_reacs['Total Reactions']
# print(len(total_reactions1))

# total_reactions2 = df2_reacs['Total Reactions']
# print(len(total_reactions2))

# bar_width = 0.35 
# r_reactions1 = np.arange(len(model_ids)) # Posiciones para Reacciones
# r_reactions2 = [x + bar_width for x in r_reactions1] # Posición DESPLAZADA para Metabolitos


# colores_bac = {
#     # Rojo/Marrón (Top 5 del póster)
#     'ST00000': '#00FF00', 
#     'ST00060': '#D4807C', # Arthrobacter
#     'ST00094': '#C76662', # Rhodococcus 
#     'ST00101': '#5F9EAD', # Pseudomonas
#     'ST00110': '#B7464C', # Pseudomonas 
#     'ST00164': '#9E3345', # Ballicus thuringesis #🤔
#     'ST00143': '#752530', # Paenibacillus
#     #Azul/Cian (Bottom 5 del póster)
#     'ST00042': '#80B6B3', # Pseudomonas umsongensis #🤔
#     'ST00109': '#3D788E', # Mycobacterium
#     'ST00154': '#26526B', # Agrobacterium
#     'ST00046': '#1A3749'  # Bacillus (Usando el color más oscuro de la escala azul)
#  }


# # colores_bac = {'#00FF00', 
# #  '#D4807C', 
# # '#C76662', 
# # '#5F9EAD', 
# #  '#B7464C', 
# #  '#9E3345',
# #  '#752530', 
# #  '#80B6B3', 
# #  '#3D788E', 
# #  '#26526B', 
# #  '#1A3749'  
# #  }

# name_bac = { 
#     'ST00000': r'$\it{Escherichia\ sp.}$',
#     'ST00060': r'$\it{Arthrobacter\ sp.}$', #✅
#     'ST00094': r'$\it{Rhodococcus\ erythropolis}$', 
#     'ST00101': r'$\it{Pseudomonas\ sp.}$', 
#     'ST00110': r'$\it{Variovorax\ paradoxus}$', 
#     'ST00164': r'$\it{Ballicus thuringesis\ sp.}$', #🤔
#     'ST00143': r'$\it{Paenibacillus\ sp.}$', #✅
#     'ST00042': r'$\it{Pseudomonas umsongensis\ sp.}$', #🤔
#     'ST00109': r'$\it{Mycobacterium\ sp.}$', #✅
#     'ST00154': r'$\it{Agrobacterium\ sp.}$', #✅
#     'ST00046': r'$\it{Bacillus\ sp.}$' #✅
# }


# plt.figure(figsize=(6, 6))

# #bar_colors = ['#5F9EAD', '#D4807C', '#00FF00', '#C76662', '#3D788E', '#1A3749']
# root = tk.Tk()
# root.title("Label Customization")
# # 1. Plotear la primera serie (Reacciones)
# plt.bar(r_reactions1, total_reactions1, 
#         color=colores_bac,
#         edgecolor='black',
#         linewidth=1.5,
#         width=bar_width,
#         hatch='/')
#         #label='dimont annotation')

# # 2. Plotear la segunda serie (Metabolitos)
# plt.bar(r_reactions2, total_reactions2, 
#         color=colores_bac,
#         width=bar_width, 
#         edgecolor='black',
#         linewidth=1.5)
#         #label='prokka annotation')


# plt.xlabel('strain ID', fontsize=12)
# plt.ylabel('number of reactions', fontsize=12)
# #plt.title('Comparación Agrupada: Tamaño de la Red Metabólica', fontsize=14)

# # Definir las etiquetas del eje X en las posiciones centrales
# plt.xticks([r + bar_width / 2 for r in r_reactions1], model_ids, rotation=45, ha='right', fontsize=10)

# plt.legend(loc='upper left')
# plt.tight_layout()
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# -----------------------------------
# Definición de Variables y Paletas
# -----------------------------------

# Nota: Asumimos que tus DataFrames df1_reacs y df2_reacs tienen el mismo orden y longitud.

colores_bac = {
    'ST00000': '#00FF00', 'ST00060': '#D4807C', 'ST00094': '#C76662', 
    'ST00101': '#5F9EAD', 'ST00110': '#B7464C', 'ST00164': '#9E3345',
    'ST00143': '#752530', 'ST00042': '#80B6B3', 'ST00109': '#3D788E', 
    'ST00154': '#26526B', 'ST00046': '#1A3749'
}

# --- Carga y Extracción de Datos (Asumido Correcto) ---
df1_reacs = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_dimont_carveme_lb_4.csv')
df2_reacs = pd.read_csv('04_resultados/rizo/biomasas/reacciones_totales_reactions_prokka_carveme_lb_4.csv')

model_ids = df1_reacs['Model ID']
total_reactions1 = df1_reacs['Total Reactions']
total_reactions2 = df2_reacs['Total Reactions']
N = len(model_ids) # Longitud de los datos

bar_width = 0.35 
r_reactions1 = np.arange(N)
r_reactions2 = [x + bar_width for x in r_reactions1] 

# --- PASO CRÍTICO: GENERAR LA LISTA DE COLORES ORDENADA ---

# Itera sobre los IDs del DataFrame y busca el color en el diccionario.
bar_color_sequence = [colores_bac.get(model_id, 'gray') for model_id in model_ids]

# -------------------------------------------------------------------------
# PLOTEO Y CONFIGURACIÓN
# -------------------------------------------------------------------------

plt.figure(figsize=(10, 6))

# 1. Plotear la primera serie (Dimont)
plt.bar(r_reactions1, total_reactions1, 
        color=bar_color_sequence, # <--- CORRECCIÓN: Usa la lista de N colores
        edgecolor='black',
        linewidth=1.5,
        width=bar_width,
        hatch='/')
        #label='Dimont Annotation')


# 2. Plotear la segunda serie (Prokka)
plt.bar(r_reactions2, total_reactions2, 
        color=bar_color_sequence, # <--- Aplica la misma secuencia de colores
        width=bar_width, 
        edgecolor='black',
        linewidth=1.5)
        #label='Prokka Annotation')


# --- CONFIGURACIÓN FINAL ---

plt.xlabel('Strain ID', fontsize=12)
plt.ylabel('Number of Reactions', fontsize=12)
plt.title('Comparison of Metabolic Network Size by Annotator', fontsize=14)

# Definir las etiquetas del eje X
plt.xticks([r + bar_width / 2 for r in r_reactions1], model_ids, rotation=45, ha='right', fontsize=10)

# 3. CAMBIAR EL COLOR DE LA LEYENDA A NEGRO (Si se desea)
legend = plt.legend(loc='upper left', frameon=False) 
for text in legend.get_texts():
    text.set_color('black')

plt.tight_layout()
plt.show()