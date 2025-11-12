# ----------------------------------------------------
# Cargar paquetes
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
#BASE_PATH = '01_data/rizo/carveme' 
# Encontrar todos los archivos CSV de biomasa
csv_files = glob.glob('04_resultados/4c/biomasas/*_prokka_carveme_lb_lb.csv')
# Diccionario para almacenar los DataFrames cargados (Modelo ID como clave)
ALL_GROWTH_DATA = {} 
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

print(f"Archivos CSV encontrados: {len(csv_files)}")
# ----------------------------------------------------
# Ciclo para cargar todos los datos 
for file_path in csv_files:    
    try:
        df = pd.read_csv(file_path)
        
        # Extraer el ID del modelo 
        file_name = os.path.basename(file_path)
        model_id = file_name.replace('_prokka_carveme_lb_lb.csv', '') 

        scientific_name = name_bac.get(model_id)
        final_label = f"{scientific_name} ({model_id})"
        
        # Almacenar el DataFrame
        ALL_GROWTH_DATA[model_id] = df
        
    except Exception as e:
        print(f"Error al cargar {file_name}: {e}")

# -----------------------------------------------------
# Ciclo graficar todas las cuvas 
plt.figure(figsize=(20, 8))

# Definir el eje de tiempo fijo (basado en la longitud del primer DataFrame)
primer_df = list(ALL_GROWTH_DATA.values())[0] 
NUM_ROWS = len(primer_df)
tiempo = np.arange(NUM_ROWS) 

# Preparar un mapa de colores para asignar un color distinto a cada línea
#colores = cm.get_cmap('viridis', len(ALL_GROWTH_DATA))
#color_index = 0

# Itera sobre el diccionario para graficar CADA MODELO
for model_id, df in ALL_GROWTH_DATA.items():
    # Extraer la biomasa (eje Y) y calcular el logaritmo
    #masa = df['Biomass (gr.)]
    masa = df.iloc[:, 1]
    log_masa = np.log10(masa + 1e-10) # Log-transformado para el crecimiento
    #log_masa = math.log10(masa)
    cepa_color = colores_bac.get(model_id, 'gray') # Busca el color Hex por el ID
    # Plotea la curva
    plt.plot(tiempo, masa, 
             linestyle='-', 
             color= cepa_color, # Asigna un color único
             label=model_id,
             ) 
    
    #color_index += 1 # Pasa al siguiente color

# ----------------------------------------------------
# 4. CONFIGURACIÓN FINAL DEL GRÁFICO
# ----------------------------------------------------

plt.title('Curvas de Crecimiento Microbiano (Escala Logarítmica)')
#plt.xlabel('Tiempo (Ciclos de Simulación)')

plt.xlabel('''Tiempo (Ciclos de Simulación)

Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe y Gapfilling con medio LB.''')


plt.ylabel('Biomasa [ln(g)]')
#texto_descriptivo = "Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe \ny Gapfilling con medio LB."

#plt.figtext(1.05, 0.5, texto_descriptivo, 
            #horizontalalignment='left', # Alinea el texto a la izquierda
            #verticalalignment='center',
            #wrap=True) # Permite el salto de línea
#plt.legend(title= 'Genomas anotados con Prokka, modelo reconstruido con Carve me y Gapfilling con medio LB, medio de crecimento LB'
           #, loc='center')
#plt.plot('Fig1. Genomas anotados con Prokka,\nmodelo reconstruido con Carve me\ny Gapfilling con medio LB,\nmedio de crecimento LB')
         #loc='center')
#texto_descriptivo = "Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe \ny Gapfilling con medio LB."
#fig = plt.subplot()
#fig.text(0.5, -0.50,"Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe \ny Gapfilling con medio LB.",
          #ha='center', fontsize=10, style='italic')
# Ajuste la posición Y (y= -0.15) y la alineación horizontal (x=0.5, 'center')
#plt.figtext(0.5, -0.15, texto_descriptivo, 
            #horizontalalignment='center', # CORRECCIÓN: Centra el texto
            #verticalalignment='center',
            #wrap=True) # Permite el salto de línea
#texto_descriptivo = (
    #"Fig. 1. Genomas anotados con Prokka, modelo reconstruido con CarveMe.\n"
    #"Simulación Batch individual con Gapfilling en medio LB."


#plt.figtext(0.5, -0.15, texto_descriptivo, 
            #horizontalalignment='center', # Centra el texto debajo del eje X
            #verticalalignment='center',
            #fontsize=10, 
            #wrap=True)
#plt.subplots_adjust(bottom=0.2)
plt.grid(True, linestyle='--', alpha=0.6)
# Muestra la leyenda con todos los IDs de los modelos
plt.legend(title='Strain', bbox_to_anchor=(1.02, 0.5), loc='center') 
output_folder = '04_resultados/4c/graficas'
output_path = os.path.join(output_folder, "comparacion_curvas__prokka_carveme_lb_lb.png")
plt.savefig(output_path)


plt.show()
