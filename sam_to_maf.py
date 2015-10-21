#!usr/bin/env python
import sys

script, aligned_to, sam_aln, maf_aln = sys.argv

with open(aligned_to, 'r') af f:
  ## creates hash/dict with key:chromosome name mapping to chromosome seq
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

## flag info: https://broadinstitute.github.io/picard/explain-flags.html
## format specifications: https://genome.ucsc.edu/FAQ/FAQformat.html

line_num = 0

for line in sam_file:
    
  ## progress indicator
    if line_num % 200000 == 0:
        print(".",end="")
        sys.stdout.flush()
    line_num += 1

    if line[0] == "@":
        continue
    read_aln = line.split('\t')

  ## getting read info from name
  ## format from genome_to_reads.py: name_index_l+length_win+windownumber
    read_info = read_aln[0]
    read_info = read_info.split('_')
    read_chr_name = read_info[0]
    read_chr_index = read_info[1]
    read_len = read_info[2][1:]

  ## getting ref info and alignment information
    flag = read_aln[1]
    if flag == 4: # read unmapped
        continue
    chromosome = read_aln[2]
    chr_index = int(read_aln[3]) - 1
  ## read sequence
    read = read_aln[9]

  ## getting cigar and assigning variables for cigar traversal
    cigar = read_aln[4]
    cigar_index = 0
    read_index = 0
    local_read_aln = []
    local_ref_aln = []

  ## going through cigar string to get sequences back
    while cigar_index < len(cigar):
        operation = cigar[cigar_index]
        cigar_index += 1
        cigar_num = ""
        while not cigar[cigar_index].isalpha():
            cigar_num += cigar[cigar_index]
            cigar_index += 1
        op_length = int(cigar_num)
        if operation == "M": # matching bases
            local_read_aln.append(read[read_index:read_index+op_length])
            local_chr_aln.append(chr_seq[chromosome][chr_index:chr_index+op_length])
            read_index += op_length
            chr_index += op_length
        elif operation == "I": # gap in ref
            local_read_aln.append(read[read_index:read_index+op_length])
            local_chr_aln.append("-"*(op_length-1))
            read_index += op_length
        elif operation == "D": # gap in read
            local_read_aln.append("-"*(op_length-1))
            local_chr_aln.append(chr_seq[chromosome][chr_index:chr_index+op_length])
            chr_index += op_length
    local_read_aln = ''.join(local_read_aln)
    local_chr_aln = ''.join(local_chr_aln)

  ## writing read alignments to file
