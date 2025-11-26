import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#leer los archivos csv
df1 = pd.read_csv('04_resultados/rizo/reacciones/variables_dimont.csv')
df2 = pd.read_csv('04_resultados/rizo/reacciones/variables_eggnog.csv')
df3 = pd.read_csv('04_resultados/rizo/reacciones/variables_prokka.csv')

#merge es para combinar dos bases de datos basados en una columna en comun, esta la extraen con el argumento ''on''
#El argumento suffixes toma una secuencia de dos elementos, donde el primer elemento 
#es el sufijo para las columnas del DataFrame de la izquierda y el segundo es para las columnas del DataFrame de la derecha.

df = (
    df1.merge(df2, on=("Model ID"))
       .merge(df3, on=("Model ID"))
)

print(df)

#para organizar los datos como un data frame con el argumento pd.DataFeame
#primero se definen las columnas: variable, anotacion y número 
#para este último, de número, se extrae cada coluna de la database que ya se mezclo con merge
long_df = pd.DataFrame({
    "Variable": ["Reacciones"]*len(df)*3 + ["Metabolitos"]*len(df)*3 + ["Genes"]*len(df)*3,
    "Anotación": (["Dimont"]*len(df) + ["EggNOG"]*len(df) + ["Prokka"]*len(df)) * 3,
    "Numero": pd.concat([
        df["Total Reactions dimont"], df["Total Reactions eggnog"], df["Total Reactions prokka"],
        df["Total Metabolites dimont"], df["Total Metabolites eggnog"], df["Total Metabolites prokka"],
        df["Total Genes dimont"],      df["Total Genes eggnog"],      df["Total Genes prokka"]
    ], ignore_index=True)
})

print(long_df)

variables = ["Reacciones", "Metabolitos", "Genes"]
anotacion = ["Dimont", "EggNOG", "Prokka"]
colores = {"Dimont": '#C8F2C2', "EggNOG": "#E8C9F0", "Prokka": '#FFB7CE'}


plt.figure(figsize=(10, 6))

positions = []
data_box = []
colors_box = []

for i, var in enumerate(variables):
    for j, metodo in enumerate(anotacion):
        subset = long_df[(long_df["Variable"] == var) & (long_df["Anotación"] == metodo)]["Numero"]
        
        positions.append(i*4 + j) 
        data_box.append(subset)
        colors_box.append(colores[metodo])

box = plt.boxplot(
    data_box,
    positions=positions,
    patch_artist=True,
    widths=0.7
)

for patch, color in zip(box['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

plt.xticks([1, 5, 9], variables, fontsize=12)

plt.ylabel("Número de elementos", fontsize=12)
plt.title("Comparación por método de anotación", fontsize=14)

handles = [plt.Line2D([0], [0], color=colores[m], linewidth=10) for m in anotacion]
plt.legend(handles, anotacion, title="Anotación", loc="upper right")

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

