# 1. lyb
library(tidyverse)
library(stringr)

colores_bac <- c(
  'ST00000' = '#00FF00', 
  'ST00060' = '#D4807C', 
  'ST00094' = '#C76662', 
  'ST00101' = '#5F9EAD', 
  'ST00110' = '#B7464C', 
  'ST00164' = '#9E3345', 
  'ST00143' = '#752530', 
  'ST00042' = '#80B6B3', 
  'ST00109' = '#3D788E', 
  'ST00154' = '#26526B', 
  'ST00046' = '#1A3749'
)

name_bac <- c(
  'ST00000' = 'Escherichia sp.', 
  'ST00060' = 'Arthrobacter sp.', 
  'ST00094' = 'Rhodococcus erythropolis', 
  'ST00101' = 'Pseudomonas sp.', 
  'ST00110' = 'Variovorax paradoxus', 
  'ST00164' = 'Ballicus thuringesis sp.', 
  'ST00143' = 'Paenibacillus sp.', 
  'ST00042' = 'Pseudomonas umsongensis', 
  'ST00109' = 'Mycobacterium sp.', 
  'ST00154' = 'Agrobacterium sp.', 
  'ST00046' = 'Bacillus sp.'
)

# 2. Path
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomasas/comunidades"

lista_archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$", full.names = TRUE)
lista_archivos <- lista_archivos[str_order(lista_archivos, numeric = TRUE)]

# 3. for cicle
lista_resultados <- list()

for (i in lista_archivos) {
  community_data <- read.csv(i)
  # Extrac 10th row to get final biomass of the bacteria strains
  biomass <- community_data[10, 2:6]
  # Total sum of the row (frequency)
  total <- sum(biomass, na.rm = TRUE)
  # Calculate frequency
  frequency <- biomass / total
  
  # Save just the name of de csv file, it will work for the plot
  frequency$community_id <- gsub("\\.csv$", "", basename(i))
  lista_resultados[[i]] <- frequency
}

# 4. Reshape data to long format for ggplot compatibility
#  Bind any number of data frames by row
data_final <- bind_rows(lista_resultados)

# Convert community_id to a factor and sort numerically to avoid the 1, 10, 11, 2 sequence with 'str_orde'
# Use 'unique' to get distinct IDs and prevent duplicated levels in the factor.
# Convert community_id to a factor to preserve the custom numerical order in the plot axes.
data_final$community_id <- factor(data_final$community_id, 
                                  levels = unique(data_final$community_id[str_order(data_final$community_id, numeric = TRUE)]))

# Reshape data from wide to long format so ggplot can map strains to colors and values to bar height.
data_long <- pivot_longer(data_final, 
                          cols = -community_id, 
                          names_to = "strains", 
                          values_to = "relative_frequency")

# 5. Generate stacked bar plot with customized labels 
ggplot(data_long, aes(x = community_id, y = relative_frequency, fill = strains)) + 
  geom_bar(position = "stack", stat = "identity", color = "black") + # Usamos color="black" para el borde de las barras
  scale_fill_manual(values = colores_bac, labels = name_bac, na.value = "gray") + # Aquí aplicamos tus diccionarios
  theme_minimal() +
  labs(title = "Composición Relativa de Cepas por Comunidad",
       x = "ID Comunidad", 
       y = "Frecuencia Relativa",
       fill = "Cepa") +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5),
        legend.text = element_text(face = "italic")) # Formato científico para la leyenda