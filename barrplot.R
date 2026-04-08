# 1. Cargar los datos

paths <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8'

data1 <- read.csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8')
data2 <- read.csv('/home/abigaylmontantearenas/Documents/proyecto_tesis/04_results/rizo/biomass_indiv')

# 2. Definir los renglones específicos (puntos de tiempo) que quieres comparar
renglones <- c(11, 21, 31, 41, 51, 61, 71, 81)

# 3. Extraer Tiempo y Biomasas SOLO para esos renglones
# Usamos el mismo índice [renglones] para todos para que coincidan
data_time   <- data1$t[renglones]
data_ST46   <- data1$ST00046[renglones]

data_ST154  <- data2$ST00154[renglones]

# 4. Crear la matriz para el gráfico (solo con los valores de biomasa)
# rbind pondrá una fila para ST46 y otra para ST154
biomassa_matrix <- rbind(data_ST46, data_ST154)

# 5. Generar el gráfico de barras agrupadas
barplot(biomassa_matrix, 
        beside = TRUE, 
        names.arg = round(data_time, 1), # El tiempo redondeado como etiquetas en el eje X
        xlab = "Time (hours)", 
        ylab = "Biomass (g)", 
        main = "Bacterial Growth Comparison: ST00046 vs ST00154", 
        col = c("grey25", "lightgrey"), 
        legend.text = c("ST00046", "ST00154"), 
        args.legend = list(x = "topleft", bty = "n"))


# --------------------------------------------------------------------------------
# 1. DEFINIR RUTAS (Asegúrate de que terminen con /)
path_mapa  <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/carpetaremota/02_data/rizo/syncoms.csv'
path_indiv <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/04_results/rizo/biomass_indiv/'
path_comm_folder  <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8/'

# 2. CARGAR EL MAPA (Para saber qué cepas hay en cada R)
mapa <- read.csv(path_mapa)
renglones_puntos <- c(11, 21, 31, 41, 51, 61, 71, 81)

# 3. SELECCIONAR QUÉ COMUNIDAD QUIERES COMPARAR (Ejemplo: Comunidad 1 de ese folder)
i <- 1 
columna_r <- paste0("R", i) # Esto busca la columna R1, R2, etc. en el mapa

# Cargar el archivo de comunidad
file_comm <- paste0(path_comm_folder, "comunidad_", i, ".csv")

if (file.exists(file_comm)) {
  data_comm <- read.csv(file_comm)
  
  # Identificar las cepas que están en esta comunidad (donde R = 1)
  cepas_en_comu <- mapa$strain[mapa[[columna_r]] == 1]
  
  # 4. CICLO PARA COMPARAR CADA CEPA CONTRA SÍ MISMA (Solo vs Mix)
  for (cepa_id in cepas_en_comu) {
    
    # Buscar el índice de la cepa para encontrar su archivo individual
    idx_cepa <- which(mapa$strain == cepa_id)
    file_indiv <- paste0(path_indiv, "comunidad_", idx_cepa, ".csv")
    
    if (file.exists(file_indiv)) {
      data_indiv <- read.csv(file_indiv)
      
      # EXTRAER DATOS DE LA MISMA CEPA EN AMBOS ARCHIVOS
      # Usamos el mismo ID (cepa_id) para ambas extracciones
      biom_solo <- data_indiv[renglones_puntos, cepa_id]
      biom_mix  <- data_comm[renglones_puntos, cepa_id]
      tiempo    <- data_comm$t[renglones_puntos]
      
      # 5. CREAR MATRIZ Y GRAFICAR
      biomassa_matrix <- rbind(biom_solo, biom_mix)
      
      barplot(biomassa_matrix, 
              beside = TRUE, 
              names.arg = round(tiempo, 1),
              col = c("grey25", "lightgrey"), 
              main = paste("Comparativa Cepa:", cepa_id, "en", columna_r),
              xlab = "Tiempo (h)", 
              ylab = "Biomasa (g)",
              legend.text = c("Individual (Solo)", "En Comunidad (Mix)"),
              args.legend = list(x = "topleft", bty = "n"))
      
      message(paste("Graficada comparación para:", cepa_id))
      
    } else {
      message(paste("No se encontró archivo individual para:", cepa_id))
    }
  }
} else {
  message(paste("No se encontró el archivo de comunidad:", file_comm))
}
##################################################################
# Vector de colores (Equivalente al diccionario colores_bac)
colores_bac <- c(
  'ST00000' = '#00FF00', 'ST00060' = '#D4807C', 'ST00094' = '#C76662', 
  'ST00101' = '#5F9EAD', 'ST00110' = '#B7464C', 'ST00164' = '#9E3345', 
  'ST00143' = '#752530', 'ST00042' = '#80B6B3', 'ST00109' = '#3D788E', 
  'ST00154' = '#26526B', 'ST00046' = '#1A3749'
)

# Vector de nombres (Sin los símbolos $ de LaTeX, los pondremos con bquote)
name_bac <- c(
  'ST00000' = 'Escherichia sp.', 'ST00060' = 'Arthrobacter sp.', 
  'ST00094' = 'Rhodococcus erythropolis', 'ST00101' = 'Pseudomonas sp.', 
  'ST00110' = 'Variovorax paradoxus', 'ST00164' = 'Ballicus thuringesis sp.', 
  'ST00143' = 'Paenibacillus sp.', 'ST00042' = 'Pseudomonas umsongensis', 
  'ST00109' = 'Mycobacterium sp.', 'ST00154' = 'Agrobacterium sp.', 
  'ST00046' = 'Bacillus sp.'
)

# --- RUTAS ---
path_mapa  <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/carpetaremota/02_data/rizo/syncoms.csv'
path_indiv <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/04_results/rizo/biomass_indiv/'
path_comm_folder <- '/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8/'

mapa <- read.csv(path_mapa)
renglones_puntos <- c(11, 21, 31, 41, 51, 61, 71, 81)

# Seleccionamos la Comunidad 1 (o la que desees) del folder
i <- 1 
columna_r <- paste0("R", i)
file_comm <- paste0(path_comm_folder, "comunidad_", i, ".csv")

if (file.exists(file_comm)) {
  data_comm <- read.csv(file_comm)
  cepas_en_comu <- mapa$strain[mapa[[columna_r]] == 1]
  
  for (cepa_id in cepas_en_comu) {
    idx_cepa <- which(mapa$strain == cepa_id)
    file_indiv <- paste0(path_indiv, "comunidad_", idx_cepa, ".csv")
    
    if (file.exists(file_indiv)) {
      data_indiv <- read.csv(file_indiv)
      
      biom_solo <- data_indiv[renglones_puntos, cepa_id]
      biom_mix  <- data_comm[renglones_puntos, cepa_id]
      tiempo    <- data_comm$t[renglones_puntos]
      
      # Seleccionar el color de la cepa y una versión más clara para el mix
      color_base <- colores_bac[cepa_id]
      # Para diferenciar, el mix puede ser el mismo color pero con transparencia (alpha)
      # O simplemente usar dos colores fijos. Aquí usamos tu color para el individual:
      colores_barras <- c(color_base, "#D3D3D3") # Color cepa vs Gris claro
      
      biomassa_matrix <- rbind(biom_solo, biom_mix)
      
      # Graficar con Título Científico (Cursivas)
      # bquote permite usar el nombre del vector y ponerlo en cursivas (italic)
      titulo_cientifico <- bquote(italic(.(name_bac[cepa_id])) ~ "en" ~ .(columna_r))
      
      barplot(biomassa_matrix, 
              beside = TRUE, 
              names.arg = round(tiempo, 1),
              col = colores_barras, 
              main = titulo_cientifico,
              xlab = "Tiempo (h)", 
              ylab = "Biomasa (g)",
              legend.text = c("Individual", "En Comunidad"),
              args.legend = list(x = "topleft", bty = "n"))
      
    }
  }
}

# -------------------------------------------------------------------------------------------

# Definir la ruta
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8"

# Verificar si la carpeta existe
if (dir.exists(ruta_carpeta)) {
  print("La ruta es correcta")
} else {
  stop("La ruta no existe. Revisa si hay algún error de dedo.")
}

# Listar los archivos (por ejemplo, si son archivos .csv)
archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$", full.names = TRUE)
print(archivos)

library(tidyverse)

# Leer todos los CSV y combinarlos en uno solo
datos_biomasa <- archivos %>% 
  map_df(~read_csv(.x) %>% mutate(archivo_origen = basename(.x)))

# Ver las primeras filas
head(datos_biomasa)



library(tidyverse)

# 1. Definir la ruta que proporcionaste
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8"

# 2. Listar y leer todos los archivos de la carpeta
# Asumiendo que son archivos .csv o .txt generados por tus simulaciones
archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$|\\.txt$", full.names = TRUE)

if (length(archivos) == 0) {
  stop("No se encontraron archivos en la carpeta. Verifica la extensión (.csv o .txt).")
}

# Leer todos los archivos y combinarlos
# Se añade una columna 'comunidad' basada en el nombre del archivo (ej. R1, R2...)
datos_comunidad <- archivos %>%
  map_df(~read_table(.x) %>% # O read_csv según el formato de tus archivos
           mutate(comunidad = basename(.x)))

# 3. Filtrar por la última hora (Estado Estacionario / Final del experimento)
# Esto es lo que sueles usar en tu tesis para comparar biomasas finales
datos_finales <- datos_comunidad %>%
  group_by(comunidad, strain) %>% # 'strain' o la columna que use tu simulador
  filter(time == max(time)) %>%
  ungroup()

# 4. Generar la Gráfica de Barras
# Esta gráfica muestra la biomasa de cada cepa en la Comunidad 8
grafica_biomasa <- ggplot(datos_finales, aes(x = reorder(strain, -biomass), y = biomass, fill = strain)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  # Si tienes réplicas (R1, R2...) dentro de la carpeta, puedes facetar:
  facet_wrap(~comunidad) + 
  labs(
    title = "Composición de Biomasa - Comunidad 8",
    subtitle = "Estado final de la simulación (última hora)",
    x = "Cepa (Strain)",
    y = "Biomasa Absoluta",
    fill = "Cepa"
  ) +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "bottom"
  )

# 5. Visualizar y guardar
print(grafica_biomasa)

# Guardar el resultado en la misma carpeta de resultados
# ggsave(file.path(ruta_carpeta, "grafica_barras_comunidad_8.png"), width = 10, height = 7)






library(tidyverse)

# 1. Definir la ruta que proporcionaste
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8"

# 2. Listar y leer todos los archivos de la carpeta
# Asumiendo que son archivos .csv o .txt generados por tus simulaciones
archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$|\\.txt$", full.names = TRUE)

if (length(archivos) == 0) {
  stop("No se encontraron archivos en la carpeta. Verifica la extensión (.csv o .txt).")
}

# Leer todos los archivos y combinarlos
# Se añade una columna 'comunidad' basada en el nombre del archivo (ej. R1, R2...)
datos_comunidad <- archivos %>%
  map_df(~read_table(.x) %>% # O read_csv según el formato de tus archivos
           mutate(comunidad = basename(.x)))

# 3. Filtrar por la última hora (Estado Estacionario / Final del experimento)
# Esto es lo que sueles usar en tu tesis para comparar biomasas finales
datos_finales <- datos_comunidad %>%
  group_by(comunidad, strain) %>% # 'strain' o la columna que use tu simulador
  filter(time == max(time)) %>%
  ungroup()

# 4. Generar la Gráfica de Barras
# Esta gráfica muestra la biomasa de cada cepa en la Comunidad 8
grafica_biomasa <- ggplot(datos_finales, aes(x = reorder(strain, -biomass), y = biomass, fill = strain)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  # Si tienes réplicas (R1, R2...) dentro de la carpeta, puedes facetar:
  facet_wrap(~comunidad) + 
  labs(
    title = "Composición de Biomasa - Comunidad 8",
    subtitle = "Estado final de la simulación (última hora)",
    x = "Cepa (Strain)",
    y = "Biomasa Absoluta",
    fill = "Cepa"
  ) +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "bottom"
  )

# 5. Visualizar y guardar
print(grafica_biomasa)

# Guardar el resultado en la misma carpeta de resultados
# ggsave(file.path(ruta_carpeta, "grafica_barras_comunidad_8.png"), width = 10, height = 7)
# ijosdjifds






#####################################################################################

ruta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8/"

archivos <- list.files(
  path = ruta,
  pattern = "^comunidad_.*\\.csv$",
  full.names = TRUE
)

comunidades <- lapply(archivos, read.csv)
names(comunidades) <- basename(archivos)

r1 <- comunidades[["comunidad_1.csv"]]
r2 <- comunidades[["comunidad_2.csv"]]
r3 <- comunidades[["comunidad_3.csv"]]
r4 <- comunidades[["comunidad_4.csv"]]
r5 <- comunidades[["comunidad_5.csv"]]
r6 <- comunidades[["comunidad_7.csv"]]


sumas_por_comunidad <- sapply(archivos, function(f) {
  df <- read.csv(f)
  ultimo_renglon <- df[nrow(df), ]
  
  # excluir primera y última columna
  valores <- ultimo_renglon[ , -c(1, ncol(df))]
  
  sum(as.numeric(valores), na.rm = TRUE)
})

# nombres del vector
names(sumas_por_comunidad) <- gsub(".csv", "", basename(archivos))

sumas_por_comunidad
# Load ggplot2
library(ggplot2)

# Create data
data <- sumas_por_comunidad(
  name=c("A","B","C","D","E") ,  
  value=c(3,12,5,18,45)
)

ggplot(data, aes(x = name, y = value, fill = name)) + 
  geom_bar(stat = "identity") +
  scale_fill_manual(values = c("orange", "pink", "blue", "red", "purple")) +
  coord_flip()
  
data <- data.frame(
  name  = names(sumas_por_comunidad),
  value = as.numeric(sumas_por_comunidad)
)

library(ggplot2)

ggplot(data, aes(x = name, y = value, fill = name)) + 
  geom_bar(stat = "identity") +
  scale_fill_manual(values = c("orange", "pink", "blue", "red", "purple", "green")) +
  coord_flip() +
  theme_minimal() +
  labs(
    x = "Comunidad",
    y = "Biomasa final total",
    title = "Biomasa final por comunidad"
  )


##################################

















library(tidyverse)

# 1. Definir la ruta que proporcionaste
ruta_carpeta <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/biomass_comunidad_8"

# 2. Listar y leer todos los archivos de la carpeta
# Asumiendo que son archivos .csv o .txt generados por tus simulaciones
archivos <- list.files(path = ruta_carpeta, pattern = "\\.csv$|\\.txt$", full.names = TRUE)

if (length(archivos) == 0) {
  stop("No se encontraron archivos en la carpeta. Verifica la extensión (.csv o .txt).")
}

# Leer todos los archivos y combinarlos
# Se añade una columna 'comunidad' basada en el nombre del archivo (ej. R1, R2...)
datos_comunidad <- archivos %>%
  map_df(~read_table(.x) %>% # O read_csv según el formato de tus archivos
           mutate(comunidad = basename(.x)))

# 3. Filtrar por la última hora (Estado Estacionario / Final del experimento)
# Esto es lo que sueles usar en tu tesis para comparar biomasas finales
datos_finales <- datos_comunidad %>%
  group_by(comunidad, strain) %>% # 'strain' o la columna que use tu simulador
  filter(time == max(time)) %>%
  ungroup()

# 4. Generar la Gráfica de Barras
# Esta gráfica muestra la biomasa de cada cepa en la Comunidad 8
grafica_biomasa <- ggplot(datos_finales, aes(x = reorder(strain, -biomass), y = biomass, fill = strain)) +
  geom_bar(stat = "identity", position = "dodge", color = "black") +
  # Si tienes réplicas (R1, R2...) dentro de la carpeta, puedes facetar:
  facet_wrap(~comunidad) + 
  labs(
    title = "Composición de Biomasa - Comunidad 8",
    subtitle = "Estado final de la simulación (última hora)",
    x = "Cepa (Strain)",
    y = "Biomasa Absoluta",
    fill = "Cepa"
  ) +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "bottom"
  )

# 5. Visualizar y guardar
print(grafica_biomasa)

# Guardar el resultado en la misma carpeta de resultados
# ggsave(file.path(ruta_carpeta, "grafica_barras_comunidad_8.png"), width = 10, height = 7)
