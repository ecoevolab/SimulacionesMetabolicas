base_path <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/resultados2/com1/biomass.txt"

df <- read.table(base_path)
colnames(df) <- c("time", "c2", "c3", "model", "biomass")
df$hours <- df$time * 0.1

# Analyze one column
gc_fit <- SummarizeGrowth(df$hours, df$biomass)
# Inspect results
print(gc_fit)
# Plot the fit
plot(gc_fit)




################################
base_path <- "/home/abigaylmontantearenas/Documents/proyecto_tesis/04_resultados/rizo/resultados2"

# buscar carpetas
op_dirs <- list.dirs(base_path, recursive = FALSE)
op_dirs <- op_dirs[grepl("/com", op_dirs)]
biomass_files <- file.path(op_dirs, "biomass.txt")
biomass_files <- biomass_files[file.exists(biomass_files)]

for (file_path in biomass_files) {
  df <- read.table(file_path)
  colnames(df) <- c("time", "c2", "c3", "model", "biomass")
  df$time <- as.numeric(df$time)
  df$hours <- df$time * 0.1
  df$biomass <- as.numeric(df$biomass)
  gc_fit <- SummarizeGrowth(df$hours, df$biomass)
  print(gc_fit)
}
  