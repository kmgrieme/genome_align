#!usr/bin/env python

## VERY incomplete at the moment, just the start of it

import sys

script, aligned_to, sam_aln, maf_aln = sys.argv

with open(aligned_to, 'r') af f:
    chr_seq = dict()
    line_num = 0
    for line in f:
        if line[0] == ">":
            current_chr = line[1:].rstrip()
            print("\nGetting full data from %s." % current_chr)
            chr_seq[current_chr] = []
            line_num += 1
            continue
        chr_seq[current_chr].append(line.rstrip())
        line_num += 1
        if line_num % 50000 == 0:
            print(".",end="")
            sys.stdout.flush()
 
print("\nJoining strings.")
for key in chr_seq:
    chr_seq[key] = "".join(chr_seq[key])
print("Reference genome data collection complete.")

print("\nOpening SAM format alignment file.")
sam_file = open(sam_aln, "r")
print("Creating MAF format alignment file.")
maf_file = open(maf_aln, "w")

maf_file.write("##maf version=1\n")

for line in sam_file:
    if line[0] == "@":
         continue
    read_aln = line.split('\t')
    flag = read_aln[1]
    chromosome = read_aln[2]
    chr_index = read_aln[3] - 1
    cigar = read_aln[4]
    read = read_aln[9]
