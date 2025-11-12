import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
# -----------------------------------
csv_files = glob.glob('./04_resultados/4c/biomasas/*_prokka_carveme_lb_lb.csv')
colores_bac = {
    # Rojo/Marrón (Top 5 del póster)
    'Escherichia_coli': '#00FF00', 
    'Bacillus_altitudinis': '#D4807C', 
    'Bacillus_atrophaeus': '#1A3749',
    'Bacillus_infantis': '#C76662',
    'Bacillus_thuringiensis': '#B7464C',
    'Corynebacterium_sp': '#9E3345', 
    'Metabacillus_indicus': '#752530', 
    # Azul/Cian (Bottom 5 del póster)
    'Micrococcus_luteus': '#80B6B3', 
    'Priestia_megaterium': '#5F9EAD', 
    'Staphylococcus_arlettae': '#3D788E', 
    'Staphylococcus_shinii': '#26526B'
}
name_bac = {
    'Escherichia_coli': r'$\it{Escherichia\ coli}$',
    'Bacillus_altitudinis': r'$\it{Bacillus\ altitudinis}$', 
    'Bacillus_atrophaeus': r'$\it{Bacillus\ atrophaeus}$',
    'Bacillus_infantis': r'$\it{Ballicus\ infantis}$', 
    'Bacillus_thuringiensis': r'$\it{Ballicus\ thuringesis}$', 
    'Corynebacterium_sp': r'$\it{Corynebacterium\ sp.}$', 
    'Metabacillus_indicus': r'$\it{Metabacillus\ indicus}$', 
    'Micrococcus_luteus': r'$\it{Micrococcus\ luteus}$',
    'Priestia_megaterium': r'$\it{Priestia\ megaterium}$', 
    'Staphylococcus_arlettae': r'$\it{Staphylococcus\ arlettae}$', 
    'Staphylococcus_shinii': r'$\it{Staphylococcus\ shinii}$', 
}

for file in csv_files:
    file_name = os.path.basename(file)
    model_id = file_name.replace('_prokka_carveme_lb_lb.csv', '')
    scientific_name = name_bac.get(model_id)
    final_label = f"{scientific_name} ({model_id})"
    cepa_color = colores_bac.get(model_id, 'black')
    try:
        df = pd.read_csv(file)
        tiempo = df.iloc[:, 0]
        masa = df.iloc[:, 1]
        plt.figure(figsize=(8, 5))
        plt.plot(tiempo, masa, 
        marker='o', 
        linestyle='-', 
        color= cepa_color,
        label= final_label)
        plt.title(f"Curvas de Crecimiento Microbiano para {scientific_name}")
        #plt.xlabel('Tiempo (Ciclos de Simulación)')
        plt.xlabel('''Tiempo (Ciclos de Simulación)
        Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe y Gapfilling con medio LB.''')
        plt.ylabel('Biomasa [ln(g)]')
        plt.grid(True, linestyle='--', alpha=0.6)
        output_folder = '04_resultados/4c/graficas'
        output_path = os.path.join(output_folder, f"{model_id}__prokka_carveme_lb_lb.png")
        plt.savefig(output_path)
        plt.show()

# Muestra la leyenda con todos los IDs de los modelos
        plt.legend(title='Modelo ID', bbox_to_anchor=(1.05, 1), loc='upper left') 
    except Exception as e:
        print(f"Error al cargar {file_name}: {e}")

