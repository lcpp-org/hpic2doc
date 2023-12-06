#!/bin/bash
#
#SBATCH --time=00:01:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --tasks-per-node=2               # Number of MPI processes per node
#SBATCH --cpus-per-task=12               # Number of compute threads per proc
#SBATCH --job-name=hpic2                 # Name of batch job
#SBATCH --partition=eng-research         # Partition (queue)
#SBATCH --output=hpic2.o%j               # Name of batch job output file
#SBATCH --error=hpic2.e%j                # Name of batch job error file
##SBATCH --mail-user=NetID@illinois.edu  # Send email notifications
##SBATCH --mail-type=BEGIN,END           # Type of email notifications to send
###############################################################################

# OpenMP will complain if these options aren't set.
export OMP_PLACES=cores
export OMP_PROC_BIND=spread

export EXE=hpic2
export DECK=/path/to/input/deck.toml

# Run the hybrid MPI/OpenMP code
srun ${EXE} --kokkos-threads=${SLURM_CPUS_PER_TASK} --i=${DECK}
