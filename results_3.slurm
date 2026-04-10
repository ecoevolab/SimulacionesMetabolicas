#!/bin/bash
#SBATCH --job-name=3results
#SBATCH --output=%x.log
#SBATCH --error=%x.error
#SBATCH --time=100000:00:00
#SBATCH --cpus-per-task=5
#SBATCH --mem=8G

echo "========================================="
echo "Job started on: $(date)"
echo "Running on host: $(hostname)"
echo "Working directory: $(pwd)"
echo "========================================="

eval "$(mamba shell hook --shell bash)"
mamba activate python3
module load COMETS

echo "[INFO] Starting Python script at $(date)"
python comets_save_3.py
echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="
