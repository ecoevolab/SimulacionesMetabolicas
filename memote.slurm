#!/bin/bash
#SBATCH --job-name=ccmemote
#SBATCH --output=/mnt/data/sur/users/mmontante/02_resultados/logs/%x.log
#SBATCH --error=/mnt/data/sur/users/mmontante/02_resultados/logs/%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G

eval "$(mamba shell hook --shell bash)"
mamba activate memote-env

INPUT_DIR="/mnt/data/sur/users/mmontante/02_resultados/cc/models/final_models"
OUTPUT_DIR="/mnt/data/sur/users/mmontante/02_resultados/1210_resultados/cc/memote"
mkdir -p "$OUTPUT_DIR"

for model in "$INPUT_DIR"/*.xml; do
    filename=$(basename "$model")
    out="$OUTPUT_DIR/${filename%.*}.json"

    if [[ -s "$out" ]]; then
        echo "Saltando $filename (ya existe)"
        continue
    fi

    echo "[$(date +%T)] Processing $filename..."
    memote run "$model" --filename "$out.tmp"

    if [[ -s "$out.tmp" ]]; then
        mv "$out.tmp" "$out"
    else
        echo "FALLO: $filename" >> "$OUTPUT_DIR/fallidos.txt"
    fi
done
