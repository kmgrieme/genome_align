#!/usr/bin/env python

import sys
import re

def split_block(block, chr1, chr2, out):
    for strand1 in block:
        if chr1 in strand1:
            aln1 = re.split(r"\s+", strand1.strip())
            for strand2 in block:
                if chr2 in strand2:
                    aln2 = re.split(r"\s+", strand2.strip())
                    seq1 = aln1[6]
                    seq2 = aln2[6]
                    seq1_ungapped = []
                    seq2_ungapped = []
                    matches = 0
                    for i in range(len(seq1)):
                        if seq1[i] == "-" and seq2[i] == "-": continue
                        if seq1[i].isalpha() and seq2[i].isalpha(): matches += 1
                        seq1_ungapped.append(seq1[i])
                        seq2_ungapped.append(seq2[i])
                    out.write("a score=0\n")
                    out.write("s %s%s %s %s %s %s\n" % (chr1.ljust(20), aln1[2].rjust(12), 
                                aln1[3].rjust(12), aln1[4], aln1[5].rjust(12), ''.join(seq1_ungapped)))
                    out.write("s %s%s %s %s %s %s\n" % (chr2.ljust(20), aln2[2].rjust(12), 
                                aln2[3].rjust(12), aln2[4], aln2[5].rjust(12), ''.join(seq2_ungapped)))
                    out.write("\n")
    return

def reads_to_file(block, chr1, out):
    for strand in block:
        if chr1 in strand:
            aln = re.split(r"\s+", strand)
            chr_name = aln[1]
            chr_index = aln[2]
            if aln[4] == "-": continue
            seq = re.sub(r"-+", "", aln[6])
            seq = seq.upper()
            fastq_header = "@%s_%s_L%s\n"
            if len(seq) > 1000: 
                print("Warning: sequence larger than 1k bp (%s bp)" % len(seq))
            elif len(seq) < 50:
                print("Warning: sequence smaller than 50 bp (%s bp)" % len(seq))
            out.write(fastq_header % (chr_name, chr_index, len(seq)))
            out.write(seq)
            out.write("\n+\n")
            out.write("~"*len(seq)+"\n")
    return

if len(sys.argv) != 5 and len(sys.argv) != 6:
    print("run in format: script originalMAF chr1 chr2 outputMAF OPT[output_fastq]")
    quit()
elif len(sys.argv) == 5:
    script, original_maf, extract1, extract2, output_maf = sys.argv
    fastq = False
elif len(sys.argv) == 6:
    script, original_maf, extract1, extract2, output_maf, output_fastq = sys.argv
    fastq = True

in_maf = open(original_maf)
out_maf = open(output_maf, "w")
if fastq: out_fq = open(output_fastq, "w")

block = []

for line in in_maf:
    if line[0] == "#": 
        out_maf.write(line)
        continue
    elif line[0] == "a":
        continue
    elif line[0] == "\n":
        split_block(block, extract1, extract2, out_maf)
        if fastq: reads_to_file(block, extract1, out_fq)
        block = []
        continue
    block.append(line)

in_maf.close()
out_maf.close()
if fastq: out_fq.close()
