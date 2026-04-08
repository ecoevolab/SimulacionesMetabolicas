#!/bin/bash
#SBATCH --job-name=gapseq_full_pipe
#SBATCH --output=%x_%j.log
#SBATCH --error=%x_%j.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=20G

eval "$(conda shell.bash hook)"
conda activate gapseq

# Directorios
INPUT_DIR="/home/abigaylmontantearenas/Documents/proyecto_tesis/01_raw_data/rizo/fasta_files"
OUTPUT_DIR="/home/abigaylmontantearenas/Documents/proyecto_tesis/02_data"
MEDIA_FILE="/home/abigaylmontantearenas/Documents/proyecto_tesis/gapseq/dat/media/LBmed.csv"

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

for faa_path in "$INPUT_DIR"/ST00*.faa; do
    
    prefix=$(basename "$faa_path" .faa)
    
    echo "----------------------------------------------------"
    echo "Procesando Genoma: $prefix"
    echo "----------------------------------------------------"
    
    # 1. FIND: Aquí sí funciona -A diamond
    gapseq find -p all -b 200 -m auto -t auto -A diamond "$faa_path"
    
    # 2. FIND-TRANSPORT: NO usar -A diamond aquí, gapseq lo gestiona interno o usa blast por defecto
    gapseq find-transport -b 200 "$faa_path"
    
    # 3. DRAFT: 
    # Añadimos -b grampos (o gramneg) según tus bacterias de rizosfera. 
    # "auto" a veces falla si no pasas el genoma completo (.fna)
    gapseq draft -r "${prefix}.faa-all-Reactions.tbl" \
                 -t "${prefix}.faa-Transporter.tbl" \
                 -p "${prefix}.faa-all-Pathways.tbl" \
                 -c "${prefix}.faa-all-res.csv" \
                 -u 200 -l 100 -b gramneg 
    
    # 4. FILL:
    # Verificamos que el archivo .rds exista antes de intentar el gap-fill
    if [ -f "${prefix}.faa-draft.rds" ]; then
        gapseq fill -m "${prefix}.faa-draft.rds" -n "$MEDIA_FILE" -b 100
    else
        echo "ERROR: No se generó el archivo RDS para $prefix"
    fi
       
done
