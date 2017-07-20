#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --output=res_%j.txt
#
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=15000
#SBATCH --gres gpu:2
#SBATCH --gres-flags=enforce-binding

module load foss/2015.05
module load CUDA/7.5.18
module load cuDNN/5.1-CUDA-7.5.18
module load tensorflow/1.0.0
module load GCC/4.9.2-binutils-2.25
module load OpenMPI/1.8.5


srun python js_main.py $1
