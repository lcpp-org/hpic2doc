#!/bin/bash
#                                                                            
#SBATCH --time=00:01:00                  # Job run time (hh:mm:ss)
#SBATCH --nodes=1                        # Number of nodes
#SBATCH --tasks-per-node=2
#SBATCH --cpus-per-task=12
#SBATCH --job-name=hpic2_openmp_release  # Name of batch job
#SBATCH --partition=eng-research            # Partition (queue)           
#SBATCH --output=hpic2_openmp_release.o%j              # Name of batch job output file
#SBATCH --error=hpic2_openmp_release.e%j              # Name of batch job error file
##SBATCH --mail-user=NetID@illinois.edu  # Send email notifications
##SBATCH --mail-type=BEGIN,END           # Type of email notifications to send
#                                                                            
###############################################################################

# Change to the directory from which the batch job was submitted
# Note: SLURM defaults to running jobs in the directory where
# they are submitted, no need for cd'ing to $SLURM_SUBMIT_DIR

#cd ${SLURM_SUBMIT_DIR}

export OMP_NUM_THREADS=12
export OMP_PLACES=cores
export OMP_PROC_BIND=spread

EXE=~/hpic2_openmp_release/hpic2
DECK=EIRENE.toml


# Run the hybrid MPI/OpenMP code
srun ${EXE} --kokkos-threads=12 --i=${DECK}

