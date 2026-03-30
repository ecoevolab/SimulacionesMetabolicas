#!/bin/bash
#SBATCH --job-name=12syncom
#SBATCH --output=%x.log
#SBATCH --error=%x.error
#SBATCH --time=1000:00:00
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
python syncom12.py
echo "[INFO] Python script finished at $(date)"

echo "========================================="
echo "Pipeline done at: $(date)"
echo "========================================="
