#!/bin/bash
#SBATCH --job-name=ecoli
#SBATCH --output=%x.log
#SBATCH --error=%x.error
#SBATCH --time=240:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G

echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

eval "$(mamba shell hook --shell bash)"
conda activate memote-env

INPUT_DIR="02_data/rizo/carveme"
OUTPUT_DIR="04_resultados/rizo/memote"

mkdir -p "$OUTPUT_DIR"

for model in "$INPUT_DIR"/ST*.xml; do
    # Extract the filename without the path
    filename=$(basename "$model")
    
    echo "Processing $filename..."
    
memote report snapshot "$model" --filename "$OUTPUT_DIR/${filename%.*}.html"
done
