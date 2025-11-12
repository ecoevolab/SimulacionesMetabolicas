
import matplotlib.pyplot as plt
import pandas as pd
import os # Necessary for path operations

# --- Load Data (Assuming your directory structure is correct) ---
file_path = os.path.join('04_resultados/rizo/biomasas', 'reacciones_totales_consolidado.csv')
df = pd.read_csv(file_path)

# --- Extract Data ---
# X-axis: Model ID (e.g., ST00046)
model_ids = df['Model ID']
# Y-axis: Total Reactions (the height of the bar)
total_reactions = df['Total Reactions']

# --- Plotting ---

plt.figure(figsize=(10, 6))

# Create the bar plot
plt.bar(model_ids, total_reactions, color='skyblue')

# --- Configuration (Corrected and Simplified) ---

# Set the title
plt.title('Resumen de Conteo de Reacciones por Modelo', fontsize=14)

# Set the X-axis label (Only define it once!)
plt.xlabel('Modelo ID', fontsize=12) 
# Note: I removed the redundant/placeholder lines ('Visualization Library', 'Number of Enthusiasts', etc.)

# Set the Y-axis label
plt.ylabel('Número Total de Reacciones', fontsize=12)

# Rotate X-axis ticks for better readability and set the font size
plt.xticks(rotation=45, ha='right', fontsize=10)

# Adjust layout to prevent labels from being cut off
plt.tight_layout()
output_folder = '04_resultados/rizo/graficas'
output_path = os.path.join(output_folder, "reacciones_prokka_carveme_lb_lb.png")
plt.savefig(output_path)
plt.show()

