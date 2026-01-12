# ----------------------------------------------------
# 1. Cargar paquetes 
# ----------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np 
import os 

# ------------------------------------
# 2. Configurar rutas y variables
# ------------------------------------
# Encontrar archivos CSV por grupos
biomas_proka_carveme_lb_08 = sorted(glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_08hrs.csv'))
biomas_proka_carveme_lb_16 = sorted(glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_16hrs.csv'))
biomas_proka_carveme_lb_24 = sorted(glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_24hrs.csv'))
biomas_proka_carveme_lb_48 = sorted(glob.glob('./04_resultados/rizo/biomasas/ST*_prokka_carveme_lb_biomasa_48hrs.csv'))

# Agrupar las listas para el ciclo
grupos_biomasa = [biomas_proka_carveme_lb_08, biomas_proka_carveme_lb_16, biomas_proka_carveme_lb_24, biomas_proka_carveme_lb_48]
nombres_tratamiento = ["proka_carveme_lb_08hr", "_proka_carveme_lb_16hr", "_proka_carveme_lb_24hr", "_proka_carveme_lb_48hrlsls"]

output_folder = '04_resultados/rizo/graficas_2'
os.makedirs(output_folder, exist_ok=True)

# Diccionarios de estética
colores_bac = {
    'ST00000': '#00FF00', 
    'ST00060': '#D4807C', 
    'ST00094': '#C76662', 
    'ST00101': '#5F9EAD', 
    'ST00110': '#B7464C', 
    'ST00164': '#9E3345', 
    'ST00143': '#752530', 
    'ST00042': '#80B6B3', 
    'ST00109': '#3D788E', 
    'ST00154': '#26526B', 
    'ST00046': '#1A3749'
}

name_bac = { 
    'ST00000': r'$\it{Escherichia\ sp.}$', 
    'ST00060': r'$\it{Arthrobacter\ sp.}$', 
    'ST00094': r'$\it{Rhodococcus\ erythropolis}$', 
    'ST00101': r'$\it{Pseudomonas\ sp.}$', 
    'ST00110': r'$\it{Variovorax\ paradoxus}$', 
    'ST00164': r'$\it{Ballicus thuringesis\ sp.}$', 
    'ST00143': r'$\it{Paenibacillus\ sp.}$', 
    'ST00042': r'$\it{Pseudomonas\ umsongensis}$', 
    'ST00109': r'$\it{Mycobacterium\ sp.}$', 
    'ST00154': r'$\it{Agrobacterium\ sp.}$', 
    'ST00046': r'$\it{Bacillus\ sp.}$' 
}

# ----------------------------------------------------
# 3. Ciclo Principal por Tratamiento (Tiempo)
# ----------------------------------------------------
for tratamiento, grupo in enumerate(grupos_biomasa):
    # Reiniciar datos para que cada gráfica sea independiente
    ALL_GROWTH_DATA = {}
    nombre_actual = nombres_tratamiento[tratamiento]
    
    if not grupo:
        print(f"Saltando grupo {nombre_actual}: No se encontraron archivos.")
        continue

    # Cargar archivos del grupo actual
    for file_path in grupo:    
        try:
            file_name = os.path.basename(file_path)
            model_id = file_name[:7] 
            
            df = pd.read_csv(file_path)
            ALL_GROWTH_DATA[model_id] = df
        except Exception as e:
            print(f"Error al cargar {file_name}: {e}")

    # --- Generar la gráfica del tratamiento actual ---
    plt.figure(figsize=(14, 10))
    
    for model_id, df in ALL_GROWTH_DATA.items():
        # Eje X: Ciclos a Horas (timeStep = 0.1)
        tiempo_h = np.arange(len(df)) * 0.1
        
        # Eje Y: Biomasa logarítmica
        masa = df.iloc[:, 1]
        log_masa = np.log10(masa + 1e-10)

        # Configuración de estilo
        color = colores_bac.get(model_id, 'gray')
        label = name_bac.get(model_id, model_id)

        plt.plot(tiempo_h, log_masa, 
                 linestyle='-', 
                 linewidth=3, 
                 color=color, 
                 label=label) 

    # Estética de la gráfica
    plt.title(f"Curvas de Crecimiento Microbiano - Tratamiento {nombre_actual}", fontsize=20)
    plt.xlabel('Tiempo (h)', fontsize=16)
    plt.ylabel(r'Biomasa [$\log_{10}$(g)]', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Leyenda fuera de la gráfica
    plt.legend(title='Cepa Bacteriana', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

    # 4. Guardar y Cerrar
    output_path = os.path.join(output_folder, f"comparacion_{nombre_actual}.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.show() # Opcional: muestra la gráfica en la consola
    plt.close() # Crucial: limpia la memoria para la siguiente gráfica

print("--- Proceso finalizado: Todas las gráficas han sido generadas ---")