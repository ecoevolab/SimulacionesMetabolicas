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
mamba activate python3
module load COMETS

echo "[INFO] Starting Python script at $(date)"
python ecoli_mets.py
echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="
