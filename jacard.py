import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def jaccard_similarity(set_a, set_b):
    """Calcula la Similitud de Jaccard entre dos conjuntos."""
    # Intersección: elementos que ambos conjuntos comparten
    intersection = len(set_a.intersection(set_b))
    
    # Unión: todos los elementos únicos combinados
    union = len(set_a.union(set_b))
    
    # Manejar división por cero si ambos conjuntos están vacíos
    if union == 0:
        return 0.0
    
    # Jaccard = Intersección / Unión
    return intersection / union

# --- DATOS DE EJEMPLO (Analogía Microbiológica) ---

# Conjunto A: Reacciones metabólicas de la Cepa 1 (ej: E. coli)
cepa_a_reacciones = {'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8'}

# Conjunto B: Reacciones metabólicas de la Cepa 2 (ej: otra E. coli evolucionada)
cepa_b_reacciones = {'R4', 'R5', 'R6', 'R7', 'R9', 'R10', 'R11'}

# Conjunto C: Reacciones metabólicas de una Especie lejana (ej: Levadura)
cepa_c_reacciones = {'R1', 'R10', 'R12', 'R13', 'R14'}


# --- CALCULAR SIMILITUDES ---
similitudes = {
    "A vs B": jaccard_similarity(cepa_a_reacciones, cepa_b_reacciones),
    "A vs C": jaccard_similarity(cepa_a_reacciones, cepa_c_reacciones),
    "B vs C": jaccard_similarity(cepa_b_reacciones, cepa_c_reacciones)
}

print("--- Similitud de Jaccard Calculada ---")
for key, value in similitudes.items():
    print(f"Jaccard {key}: {value:.3f}")
# El resultado de A vs B (4/11 ≈ 0.364) es el más alto, como se espera entre cepas cercanas.

# Crear el DataFrame para Matplotlib
jaccard_df = pd.DataFrame(list(similitudes.items()), columns=['Par de Cepas', 'Jaccard'])

# Añadir una columna de "Grupo" para simular los diferentes colores de tu gráfico
# En este caso, solo tienes tres puntos. Para simular el estilo del artículo, 
# se graficarán como puntos individuales.
jaccard_df['X_Posicion'] = [1, 2, 3] # Posición manual en el eje X

print("--- Similitud de Jaccard Calculada ---")
print(jaccard_df)
print("-" * 40)

# --- 3. CREACIÓN DE LA GRÁFICA (Estilo de dispersión simple) ---

plt.figure(figsize=(7, 5))

# Plotear los puntos. Usamos un círculo relleno ('o') y le damos un color único.
plt.plot(jaccard_df['X_Posicion'], jaccard_df['Jaccard'], 
         marker='o',         # Marcador de círculo
         linestyle='',       # Sin línea de conexión
         color='teal',       # Color del punto
         markersize=10,
         label='Comparaciones Jaccard')


# D. Configuración y Estilo Final

# Título y etiquetas
plt.title('Similitud de Reacciones (Jaccard Index)')
plt.ylabel('Jaccard Index', fontsize=12)
plt.xlabel('Par de Comparación')

# Establecer límites y ticks del eje Y (similar a la imagen del artículo)
plt.ylim(0, 0.8)
plt.yticks(np.arange(0.0, 0.81, 0.2)) 

# Etiquetas del eje X
plt.xticks(jaccard_df['X_Posicion'], jaccard_df['Par de Cepas'], rotation=0)

# Añadir rejilla y leyenda
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.show()