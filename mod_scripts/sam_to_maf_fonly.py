#!usr/bin/env python

import sys
from chromosome_lengths import *

if len(sys.argv) != 4:
    print("\nInvalid number of arguments.")
    print("Run using the format 'script ref_genome sam_alignment maf_destination'.\n")
    quit()

script, genome, sam_f, maf_f = sys.argv

#print("\nConverting %s to MAF, destination %s." % (sam_f, maf_f))
#print("\nOpening reference genome.\n")
with open(genome, "r") as f:
    line_num = 0
    chr_dict = dict()
    for line in f:
        if line[0] == ">":
            current_chr = line[1:].rstrip()
            line_num += 1
            chr_dict[current_chr] = []
            #print("Processing data from chromosome %s." % current_chr)
            continue
        chr_dict[current_chr].append(line.rstrip())
        #print("Working on line %s." % (line_num + 1), end="\r")
        line_num += 1
    #print("%s lines processed." % (line_num + 1))
    #print("Reference genome data collection complete.")

#print("Joining chromosome strings.")
chr_lens = dict()
for key in chr_dict:
    chr_dict[key] = ''.join(chr_dict[key])
    chr_lens[key] = len(chr_dict[key])

#print("\nOpening SAM alignment file.")
sam = open(sam_f, "r")
#print("Creating MAF alignment file.")
maf = open(maf_f, "w")
maf.write("##maf version=1\n")

#print("Processing SAM alignment.\n")

line_num = 0

for line in sam:
    #print("Processing line %s of SAM file." % (line_num + 1), end="\r")
    line_num += 1

    if line[0] == "@":
        if line[0:3] == "@PG":
            maf.write("# Program parameters:\n")
            maf.write("# %s\n" % line[3:].rstrip())
        continue

    aln_info = line.split("\t")

  ## flag: determine operation
    flag = int(aln_info[1])
    if flag == 4: continue
    elif flag == 0: read_dir = "+"
    elif flag == 16: continue 

  ## info for read from fq window name + read seq
  ## format: chrname_chrindex_L+length_winX
    win_info = aln_info[0].split('_')
    read_chr = win_info[0]
    read_chr_i = int(win_info[1])
    read_len = int(win_info[2][1:])
    if read_dir == "-": 
        read_chr_i = sim_chr_len[read_chr] - (read_chr_i + read_len)
    read = aln_info[9]

  ## info for ref
    ref_chr = aln_info[2]
    ref_chr_i = int(aln_info[3]) - 1

  ## cigar string traversal setup
    cigar = aln_info[5]
    cigar_i = 0
    read_i = 0
    ref_i = ref_chr_i
    read_aln = []
    ref_aln = []


  ## cigar string traversal
    while cigar_i < len(cigar):
        op_num = ""
        while not cigar[cigar_i].isalpha():
            op_num += cigar[cigar_i]
            cigar_i += 1
        op_num = int(op_num)
        op = cigar[cigar_i]
        if op == "S": # soft clip: unaligned bases in read
            if cigar_i != (len(cigar) - 1): # skips changing index if last clip 
                read_i += op_num
                read_chr_i += op_num # change starting chromosome index
            read_len -= op_num
        elif op == "M": # match
            read_aln.append(read[read_i:read_i + op_num])
            ref_aln.append(chr_dict[ref_chr][ref_i:ref_i + op_num])
            read_i += op_num
            ref_i += op_num
        elif op == "I": # gap in ref
            read_aln.append(read[read_i:read_i + op_num])
            ref_aln.append("-" * op_num)
            read_i += op_num
        elif op == "D": # gap in read
            read_aln.append("-" * op_num)
            ref_aln.append(chr_dict[ref_chr][ref_i:ref_i + op_num])
            ref_i += op_num
        cigar_i += 1

    ref_len = ref_i - ref_chr_i

    read_aln = ''.join(read_aln)
    ref_aln = ''.join(ref_aln)

  ## writing to maf file
  ## maf alignment format:
      ## a score=x
      ## s seq_name start_index #bp_aligned direction length_chromosome seq
      ## s hg16.chr7    27707221 13 + 158545518 gcagctgaaaaca
      ## new line between each alignment, groups are how it's read
    maf.write("a score=0\n")
  ## this is the most ridiculous mess in the world ugh
    read_str = "s %s%s %s %s %s %s\n" % (read_chr.ljust(30), str(read_chr_i).rjust(12), read_len, 
                                read_dir, str(sim_chr_len[read_chr]).rjust(12), read_aln)
    ref_str = "s %s%s %s %s %s %s\n" % (ref_chr.ljust(30), str(ref_chr_i).rjust(12), ref_len, 
                                "+", str(chr_lens[ref_chr]).rjust(12), ref_aln)
    maf.write(read_str)
    maf.write(ref_str)
    maf.write("\n")

#print("%s file lines read total." % (line_num + 1))
#print("\nClosing output MAF file.")
maf.close()
#print("Conversion complete.\n")
