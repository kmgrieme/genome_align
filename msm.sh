#!/bin/sh
# Name of job
#$ -N MSMCowMouseOL195
# Make sure that the .e and .o file arrive in the working directory
#$ -cwd
# Send mail to these users
#$ -M imsailin@gmail.com
#$ -m beas
#$ -q gpu
#$ -l gpu=1
module load cuda
MaxSSmap_v2/cuda6_src/MaxSSMap dnagenome -f newCow.ChrC.fa -q ol195.fq -fl 4800 -nq 789941 -t 256 -cd 0
