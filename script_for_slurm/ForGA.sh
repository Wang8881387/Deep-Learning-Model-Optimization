#!/bin/bash
#SBATCH --nodes=1
#SBATCH --job-name=GA_parallel
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=3G
#SBATCH --output=/home/ccllab/forGA.log
#SBATCH --partition=COMPUTE2Q
#SBATCH --account=root #tmul

pip install matplotlib

srun --kill-on-bad-exit=1 --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/MainGA.py &
srun --kill-on-bad-exit=1 --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_7/MainGA2.py &
srun --kill-on-bad-exit=1 --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_30/MainGA2.py &
srun --kill-on-bad-exit=1 --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_40/MainGA2.py &
srun --kill-on-bad-exit=1 --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK python3 /home/ccllab/gaSNN/SNN_50/MainGA2.py &
wait

