#!/usr/bin/env python
import sys
import re

script, chromosome, in_maf, out_fq = sys.argv

maf = open(in_maf)
fq = open(out_fq, "w")

threshold = 200
step = 5

for line in maf:
    if line[0] == "a" or line[0] == "#": continue
    if chromosome in line:
        maf_string = re.split(r' +', line.strip())
        chr_name = maf_string[1]
        chr_index = int(maf_string[2])
        fastq_header = '@%s_%s_L%s\n'
        seq = re.sub(r'-+', '', maf_string[6])
        seq = seq.upper()
        #if len(seq) > threshold:
        #    for i in range(0, len(seq)-threshold, step):
        #        working_index = chr_index + i
        #        fq.write(fastq_header % (chr_name, working_index, threshold))
        #        fq.write(seq[i:i+threshold])
        #        fq.write("\n+\n")
        #        fq.write("~"*threshold)
        #        fq.write("\n")
        #    last_seq = seq[i+threshold:]
        #    fq.write(fastq_header % (chr_name, working_index+step, len(seq)-(i+threshold)))
        #    fq.write(last_seq)
        #    fq.write("\n+\n")
        #    fq.write("~"*(len(last_seq)))
        #    fq.write("\n")
        #else:    
        fq.write(fastq_header % (chr_name, chr_index, len(seq)))
        fq.write(seq)
        fq.write("\n+\n")
        fq.write("~"*len(seq))
            fq.write("\n")

maf.close()
fq.close()
