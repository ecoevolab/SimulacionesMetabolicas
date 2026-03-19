install.packages('readxl')
install.packages('sybilSBML')
install.packages('beeswarm')
install.packages('ggbeeswarm')
library(dplyr)
library(stringr)
library(ggplot2)
library(ggbeeswarm)
library(tidyverse)
library(stringr)
# ------------ MEMOTE BEESWARM -----------------
df_memote <- read.csv("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/memote.csv")

df_memote <- df_memote %>%
  mutate(method = str_extract(ID, "dimont|eggnog|prokka"))
df_memote
names(df_memote)

ggplot(df_memote,
       aes(x = method,
           y = score,
           color = method)) +
  geom_beeswarm(size = 3) +
  labs(
    x = "Reconstruction Method",
    y = "Memote Score"
  ) +
  theme_minimal()
# -------------- MEMOTE BOXPLOT --------------------------
df_memote <- df_memote %>%
  mutate(method = str_extract(ID, "dimont|eggnog|prokka"))

ggplot(df_memote,
       aes(x = method,
           y = score,
           fill = method)) +
  geom_boxplot(alpha = 0.6) +
  labs(
    x = "Reconstruction Method",
    y = "Memote Score"
  ) +
  theme_minimal()


# ------------ REACTIONS --------------
# leer csv
df_variables <- read.csv(
  "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/reacciones/variables_totales_kbase.csv"
)



print(df_variables)

# convertir a formato largo
long_df <- df_variables %>%
  pivot_longer(
    cols = c(Total_Reactions, Total_Metabolites, Total_Genes),
    names_to = "Variable",
    values_to = "Numero"
  )

# cambiar nombres para que se vean bien en la gráfica
long_df$Variable <- recode(
  long_df$Variable,
  Total_Reactions = "Reacciones",
  Total_Metabolites = "Metabolitos",
  Total_Genes = "Genes"
)

print(long_df)

colores <- c(
  "dimont"="#009473",
  "eggnog"="#440099",
  "prokka"="#E06195",
  "default"="#F5A327",
  "rast"="#22ABA2"
  
)

reconstruccion <- c(
  "dimont"="Dimont_LB",
  "eggnog"="EggNOG_LB",
  "prokka"="Prokka_LB",
  "default"="Default_LB",
  "rast"="Rast_LB"
)

# boxplot
p <- ggplot(
  long_df,
  aes(
    x = Variable,
    y = Numero,
    fill = Annotation
  )
) +
  geom_boxplot(
    position = position_dodge(width = 0.8),
    alpha = 0.6
  ) +
  scale_fill_manual(
    values = colores,
    labels = reconstruccion,
    name = "Reconstruction Method"
  ) +
  labs(
    y = "Number of elements",
    title = "Comparación por método de anotación"
  ) +
  theme_minimal() +
  theme(
    legend.position = "right",
    axis.text = element_text(size = 12)
  )

print(p)

# guardar figura
output_folder <- "04_resultados/rizo/graficas"

if(!dir.exists(output_folder)){
  dir.create(output_folder, recursive = TRUE)
}

output_path <- file.path(
  output_folder,
  "reconstruction_methods.png"
)

ggsave(output_path, p, width = 10, height = 6)



# ------------ INDIVIDUAL EXPERIMENTAL CURVES --------------
files <- list.files(
  "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass/individuales",
  pattern = "ST.*\\.csv",
  full.names = TRUE
)

# ------------------------------------------------------
# Carpeta de salida
# ------------------------------------------------------
output_folder <- "04_resultados/rizo/graficas_2"
dir.create(output_folder, showWarnings = FALSE)

# ------------------------------------------------------
# Colores bacterias
# ------------------------------------------------------
colores_bac <- c(
  "ST00000"="#00FF00",
  "ST00060"="#D4807C",
  "ST00094"="#C76662",
  "ST00101"="#5F9EAD",
  "ST00110"="#B7464C",
  "ST00164"="#9E3345",
  "ST00143"="#752530",
  "ST00042"="#80B6B3",
  "ST00109"="#3D788E",
  "ST00154"="#26526B",
  "ST00046"="#1A3749"
)

# ------------------------------------------------------
# Nombres científicos
# ------------------------------------------------------
name_bac <- c(
  "ST00000"="italic('Escherichia sp.')",
  "ST00060"="italic('Arthrobacter sp.')",
  "ST00094"="italic('Rhodococcus erythropolis')",
  "ST00101"="italic('Pseudomonas sp.')",
  "ST00110"="italic('Variovorax paradoxus')",
  "ST00164"="italic('Ballicus thuringesis')",
  "ST00143"="italic('Paenibacillus sp.')",
  "ST00042"="italic('Pseudomonas umsongensis')",
  "ST00109"="italic('Mycobacterium sp.')",
  "ST00154"="italic('Agrobacterium sp.')",
  "ST00046"="italic('Bacillus sp.')"
)

# ------------------------------------------------------
# Tratamientos
# ------------------------------------------------------
tratamientos <- c(
  "_prokka_carveme_lb_treat"="_prokka_carveme_treat",
  "_dimont_carveme_lb_treat"="_dimont_carveme_treat",
  "_eggnog_carveme_lb_treat"="_eggnog_carveme_treat",
  "_biomasa_08hrs"="_biomasa_08hrs",
  "_biomasa_16hrs"="_biomasa_16hrs",
  "_biomasa_24hrs"="_biomasa_24hrs",
  "_biomasa_48hrs"="_biomasa_48hrs"
)

# ------------------------------------------------------
# Función detectar tratamiento
# ------------------------------------------------------
detectar_tratamiento <- function(nombre){
  
  for(i in names(tratamientos)){
    
    if(grepl(i, nombre)){
      return(tratamientos[i])
    }
    
  }
  
  return("desconocido")
}

# ------------------------------------------------------
# Loop principal
# ------------------------------------------------------
for(file in files){
  
  file_name <- basename(file)
  model_id <- substr(file_name,1,7)
  
  treat <- detectar_tratamiento(file_name)
  
  scientific_name <- name_bac[[model_id]]
  if(is.null(scientific_name)) scientific_name <- "desconocido"
  
  color <- colores_bac[[model_id]]
  if(is.null(color)) color <- "black"
  
  final_label <- paste0(model_id,treat)
  
  tryCatch({
    
    df <- read_csv(file, show_col_types = FALSE)
    
    tiempo <- df[[1]]*0.1
    masa <- df[[2]]
    
    plot_data <- tibble(
      tiempo=tiempo,
      masa=masa
    )
    
    p <- ggplot(plot_data, aes(x=tiempo,y=masa))+
      geom_line(color=color)+
      geom_point(color=color)+
      theme_minimal()+
      labs(
        title=paste("Curvas de Crecimiento Microbiano para", scientific_name),
        x="Tiempo (horas)",
        y="Biomasa [g]"
      )
    
    output_path <- file.path(output_folder,paste0(final_label,".png"))
    
    ggsave(output_path,p,width=10,height=5)
    
  }, error=function(e){
    
    cat("Error al cargar",file_name,"\n")
    
  })
  
}


# --------------------------------------------------
# INDIVIDUAL BIOMASS CURVES 
# --------------------------------------------------
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

# ------------------------------------------------
# Nombres científicos
# ------------------------------------------------
name_bac <- c(
  ST00000 = "Escherichia sp.",
  ST00060 = "Arthrobacter sp.",
  ST00094 = "Rhodococcus erythropolis",
  ST00101 = "Pseudomonas sp.",
  ST00110 = "Variovorax paradoxus",
  ST00164 = "Ballicus thuringesis",
  ST00143 = "Paenibacillus sp.",
  ST00042 = "Pseudomonas umsongensis",
  ST00109 = "Mycobacterium sp.",
  ST00154 = "Agrobacterium sp.",
  ST00046 = "Bacillus sp."
)

# ------------------------------------------------
# Buscar archivos CSV
# ------------------------------------------------
files <- list.files(
  "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass/individuales/lb10",
  pattern="ST.*\\.csv",
  full.names=TRUE
)

# filas que quieres seleccionar
rows <- c(2,42,202,242,480,722)

# ------------------------------------------------
# Leer y unir datos
# ------------------------------------------------
datos <- map_dfr(files, function(file){
  
  model_id <- substr(basename(file),1,7)
  
  df <- read_csv(file, show_col_types = FALSE)
  
  df_sel <- df[rows, ]
  
  tibble(
    tiempo = df_sel[[3]],
    biomasa = df_sel[[2]],
    modelo = model_id
  )
})

# ------------------------------------------------
# Graficar
# ------------------------------------------------
ggplot(datos, aes(x = tiempo, y = biomasa, color = modelo, group = modelo)) +
  
  geom_line(linewidth = 1) +
  geom_point() +
  
  scale_color_manual(
    values = colores_bac,
    labels = name_bac
  ) +
  
  theme_minimal() +
  
  labs(
    title = "Curvas de crecimiento microbiano",
    x = "Tiempo (horas)",
    y = "Biomasa",
    color = "Especie"
  )


# EXPERIMENTAL 
library(tidyverse)

# ------------------------------------------------
# Colores bacterias
# ------------------------------------------------
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

# ------------------------------------------------
# Nombres científicos
# ------------------------------------------------
name_bac <- c(
  ST00000 = "Escherichia sp.",
  ST00060 = "Arthrobacter sp.",
  ST00094 = "Rhodococcus erythropolis",
  ST00101 = "Pseudomonas sp.",
  ST00110 = "Variovorax paradoxus",
  ST00164 = "Ballicus thuringesis",
  ST00143 = "Paenibacillus sp.",
  ST00042 = "Pseudomonas umsongensis",
  ST00109 = "Mycobacterium sp.",
  ST00154 = "Agrobacterium sp.",
  ST00046 = "Bacillus sp."
)

# ------------------------------------------------
# Leer datos experimentales
# ------------------------------------------------
ruta_experimental <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/05_doc/resultados_experimentales/data_test_single_strains_28.csv"

df_experimental <- read_csv(ruta_experimental, show_col_types = FALSE)

# ------------------------------------------------
# Convertir a formato largo
# ------------------------------------------------
datos_long <- df_experimental %>%
  pivot_longer(
    cols = c(`0`,`4`,`20`,`24`,`48`,`72`),
    names_to = "tiempo",
    values_to = "biomasa"
  ) %>%
  mutate(tiempo = as.numeric(tiempo))

# ------------------------------------------------
# Graficar
# ------------------------------------------------
ggplot(datos_long, aes(x = tiempo, y = biomasa, color = strain, group = strain)) +
  
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  
  scale_color_manual(
    values = colores_bac,
    labels = name_bac
  ) +
  
  theme_minimal() +
  
  labs(
    title = "Curvas de crecimiento microbiano",
    x = "Tiempo (horas)",
    y = "Biomasa",
    color = "Especie"
  )

# ---------------------------------------


# ----------------------------------------------------
# 1. Cargar paquetes
# ----------------------------------------------------
library(readr)     # leer csv
library(ggplot2)   # graficas
library(dplyr)     # manipulación de datos
library(stringr)   # manejo de strings
library(fs)        # manejo de carpetas
library(readxl)

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
############################################
ruta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass/resultados_experimentales/data_test_single_strains.xlsx"
data1 <- read_excel(ruta, sheet = "biomass")

data_long <- pivot_longer(
  data1,
  cols = -tiempo,
  names_to = "cepa",
  values_to = "OD"
)

ggplot(data_long, aes(x = tiempo, y = OD, color = cepa)) +
  geom_line() +
  geom_point() +
  labs(
    x = "Tiempo",
    y = "OD",
    title = "Curvas de crecimiento"
  ) +
  theme_minimal()
###########
library(readr)
# Reemplaza la ruta con la ubicación de tu archivo ST00042.csv
data2 <- read_csv("/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass/individuales/lb10/ST00042.csv")

library(ggplot2)

ggplot(data2, aes(x = t, y = ST00042)) +
  geom_line() +
  geom_point()

library(ggplot2)

library(ggplot2)
filas <- c(42,202,242,480,722)
subset <- data2[filas, ]
#############
ggplot(data2[c(42,202,242,480,722), ], aes(x = t, y = ST00042, group = 1)) +
  geom_line() +
  geom_point(size = 3)
################################

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