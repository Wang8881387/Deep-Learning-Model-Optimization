#!/bin/bash
#SBATCH --nodes=1
#SBATCH --job-name=GA_ALL
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=2G
#SBATCH --output=/home/ccllab/forGAALL.log
#SBATCH --partition=COMPUTE2Q
#SBATCH --account=ccllab #tmul

pip install matplotlib

srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/foralltest/gatest.py &
srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_20/foralltest/gatest.py &
srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_30/foralltest/gatest.py &
srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_40/foralltest/gatest.py &
srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_50/foralltest/gatest.py &
wait

