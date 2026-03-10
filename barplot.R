library(tidyverse)
library(stringr)
library(ggplot2)

# ------------ INDIVIDUAL BIOMASS CURVES (48 h) -----------
# ----------------------------------------------------
# 1. Cargar paquetes
# ----------------------------------------------------
library(readr)     # leer csv
library(ggplot2)   # graficas
library(dplyr)     # manipulación de datos
library(stringr)   # manejo de strings
library(fs)        # manejo de carpetas

# ----------------------------------------------------
# 2. Encontrar archivos de entrada
# ----------------------------------------------------
biomas_prokka_carveme_lb_48 <- sort(
  list.files(
    "./04_resultados/rizo/biomasas/",
    pattern = "^ST.*_prokka_carveme_lb_biomasa_48hrs.csv$",
    full.names = TRUE
  )
)

output_folder <- "04_resultados/rizo/graficas_2/individual_48hrs"
dir_create(output_folder)

# ----------------------------------------------------
# 3. Diccionarios de estética
# ----------------------------------------------------
colores_bac <- c(
  ST00000 = "#00FF00",
  ST00060 = "#D4807C",
  ST00094 = "#C76662",
  ST00101 = "#5F9EAD",
  ST00110 = "#B7464C",
  ST00164 = "#9E3345",
  ST00143 = "#752530",
  ST00042 = "#80B6B3",
  ST00109 = "#3D788E",
  ST00154 = "#26526B",
  ST00046 = "#1A3749"
)

name_bac <- c(
  ST00000 = "Escherichia sp.",
  ST00060 = "Arthrobacter sp.",
  ST00094 = "Rhodococcus erythropolis",
  ST00101 = "Pseudomonas sp.",
  ST00110 = "Variovorax paradoxus",
  ST00164 = "Ballicus thuringesis sp.",
  ST00143 = "Paenibacillus sp.",
  ST00042 = "Pseudomonas umsongensis",
  ST00109 = "Mycobacterium sp.",
  ST00154 = "Agrobacterium sp.",
  ST00046 = "Bacillus sp."
)

# ----------------------------------------------------
# 4. Loop por archivo (una figura por cepa)
# ----------------------------------------------------
for (input_file in biomas_prokka_carveme_lb_48) {
  
  # Extraer ID de la cepa
  model_id <- str_sub(basename(input_file), 1, 7)
  
  # Leer datos
  df <- read_csv(input_file, show_col_types = FALSE)
  
  growth_data <- tibble(
    time_h  = seq_len(nrow(df)) * 0.1,
    biomass = df[[2]]
  )
  
  # Gráfica individual
  p <- ggplot(growth_data, aes(x = time_h, y = biomass)) +
    geom_line(
      linewidth = 1.3,
      color = colores_bac[model_id]
    ) +
    labs(
      title = paste(
        "Individual Growth Curve (48 h) –",
        name_bac[model_id]
      ),
      x = "Time (h)",
      y = expression(italic("Biomass (g)"))
    ) +
    theme_bw(base_size = 14) +
    theme(
      plot.title = element_text(size = 16, face = "bold")
    )
  
  # Guardar figura
  output_file <- file.path(
    output_folder,
    paste0("individual_growth_", model_id, "_48hrs.png")
  )
  
  ggsave(
    filename = output_file,
    plot = p,
    width = 10,
    height = 7,
    dpi = 300
  )
}

message("Todas las curvas individuales de 48 h fueron generadas correctamente")


# ------------ COMMUNITY BIOMASS CURVE -----------
# ------------ INDIVIDUAL VS COMMUNITY BIOMASS ------
# ------------ RELATIVE FREQUENCY ----------------
# 2. Configuración de Diccionarios (Colores y Nombres Científicos)
colores_bac <- c(
  'ST00000' = '#00FF00', 'ST00060' = '#D4807C', 'ST00094' = '#C76662', 
  'ST00101' = '#5F9EAD', 'ST00110' = '#B7464C', 'ST00164' = '#9E3345', 
  'ST00143' = '#752530', 'ST00042' = '#80B6B3', 'ST00109' = '#3D788E', 
  'ST00154' = '#26526B', 'ST00046' = '#1A3749'
)

name_bac <- c(
  'ST00000' = 'Escherichia sp.', 'ST00060' = 'Arthrobacter sp.', 
  'ST00094' = 'Rhodococcus erythropolis', 'ST00101' = 'Pseudomonas sp.', 
  'ST00110' = 'Variovorax paradoxus', 'ST00164' = 'Bacillus thuringiensis sp.', 
  'ST00143' = 'Paenibacillus sp.', 'ST00042' = 'Pseudomonas umsongensis', 
  'ST00109' = 'Mycobacterium sp.', 'ST00154' = 'Agrobacterium sp.', 
  'ST00046' = 'Bacillus sp.'
)

# 3. Rutas de carpetas
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8"

# Listar y ordenar archivos numéricamente
lista_archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$", full.names = TRUE)
lista_archivos <- lista_archivos[str_order(lista_archivos, numeric = TRUE)]

# 4. Procesamiento de datos (Ciclo For)
lista_resultados <- list()

for (i in lista_archivos) {
  community_data <- read.csv(i)
  
  # Seleccionamos columnas de biomasa (excluyendo cycle y t)
  cepas_cols <- setdiff(colnames(community_data), c("cycle", "t"))
  biomass <- community_data[10, cepas_cols]
  
  # Cálculo de frecuencia relativa
  total <- sum(biomass, na.rm = TRUE)
  frequency <- biomass / total
  
  # CAMBIO DE NOMBRE: De "comunidad_1" a "R1"
  # Extraemos el número del nombre del archivo y le ponemos la R
  file_name <- gsub("\\.csv$", "", basename(i))
  num_id <- str_extract(file_name, "\\d+") # Extrae los dígitos
  frequency$community_id <- paste0("R", num_id)
  
  lista_resultados[[i]] <- frequency
}

# 5. Transformación de datos
data_final <- bind_rows(lista_resultados)

# Ordenar los IDs (R1, R2, R3...) numéricamente
orden_niveles <- str_sort(unique(data_final$community_id), numeric = TRUE)
data_final$community_id <- factor(data_final$community_id, levels = orden_niveles)

# Convertir a formato largo
data_long <- pivot_longer(data_final, 
                          cols = -community_id, 
                          names_to = "strains", 
                          values_to = "relative_frequency") %>%
  filter(!is.na(relative_frequency))

# 6. Generar el gráfico con ggplot2
grafica_final <- ggplot(data_long, aes(x = community_id, y = relative_frequency, fill = strains)) + 
  geom_bar(position = "stack", stat = "identity", color = "black", width = 0.6) + 
  scale_fill_manual(values = colores_bac, labels = name_bac) + 
  theme_minimal() +
  labs(title = "Relative Composition of Strains at 8h",
       subtitle = "Analysis of Communities R1 to R6",
       x = "Community ID", 
       y = "Relative Frequency",
       fill = "Bacterial Strains") +
  theme(axis.text.x = element_text(face = "bold"), # R1, R2... en negritas
        legend.text = element_text(face = "italic"),
        panel.grid.major.x = element_blank())

# 7. Mostrar y guardar
print(grafica_final)

ggsave("Relative_Frequency_R1_R6.png", plot = grafica_final, 
       width = 8, height = 6, dpi = 300)

# ---------------- TOTAL BIOMASS COMPARATION -----------------------------------
# =========================
# 1. RUTA Y ARCHIVOS
# =========================

ruta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8/"

archivos <- list.files(
  path = ruta,
  pattern = "^comunidad_.*\\.csv$",
  full.names = TRUE
)

# =========================
# 2. SUMA DEL ÚLTIMO RENGLÓN
#    (sin primera ni última columna)
# =========================

sumas_por_comunidad <- sapply(archivos, function(f) {
  df <- read.csv(f)
  ultimo_renglon <- df[nrow(df), ]
  
  # excluir primera (cycle) y última columna
  valores <- ultimo_renglon[, -c(1, ncol(df))]
  
  sum(as.numeric(valores), na.rm = TRUE)
})

# nombres del vector (sin .csv)
names(sumas_por_comunidad) <- gsub(".csv", "", basename(archivos))

# =========================
# 3. DATA FRAME PARA GGPLOT
# =========================

data <- data.frame(
  name  = names(sumas_por_comunidad),
  value = as.numeric(sumas_por_comunidad)
)

data$name <- paste0("R", seq_len(nrow(data)))

data

# =========================
# 4. GRÁFICA DE BARRAS
# =========================

colores_comunidad <- c(
  "#F2A541",  # mostaza suave
  "#E07A5F",  # coral apagado
  "#81B29A",  # verde salvia
  "#A5A58D",  # arena / oliva claro
  "#8D99AE",  # gris azulado
  "#BC6C25",  # café cálido
  "#3A5A40",  # verde bosque oscuro
  "#6D597A",  # morado grisáceo suave
  "#B5838D"   # rosa viejo / malva apagado
)


ggplot(data, aes(x = name, y = value, fill = name)) + 
  geom_bar(stat = "identity") +
  scale_fill_manual(values = colores_comunidad) +
  theme_minimal() +
  labs(
    x = "Community ID",
    y = "Total biomass (g)",
    #title = "Biomasa final por comunidad"
  )

# -------------- ABSOLUTE FREQUENCY ------------------------------