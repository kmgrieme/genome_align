import sys
import re

def write_block(read_chr, in_block, out_file):
    if read_chr in block[1]: return
    for line in block:
        out_file.write(line)
    out_file.write("\n")
    return

if len(sys.argv) != 4:
    print("\nrun in format script input output chr where input/output are maf\n")
    quit()

script, in_maf, out_maf, forward_chr = sys.argv

block = []

f_out = open(out_maf, "w")
with open(in_maf) as f_in:
    for line in in_maf:
        if line[0] == "#": f_out.write(line)
        elif line[0] == "\n":
            write_block(forward_chr, block, f_out)
            block = []
        else: block.append(line)

f_out.close()
