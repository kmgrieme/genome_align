import sys
import re

if sys.argv != 3:
    print("\nrun in format script input output where input/output are maf\n")
    quit()

script, in_maf, out_maf, read_chr = sys.argv

block = []

with open(in_maf) as f_in:
    with open(out_maf, "w") as f_out:
        for line in f_in:
            if line.strip() == "":
                if block:
                block = []
            elif line[0] == "a" or line[0] == "s":
                if read_chr in line:
                    if re.split(r"\s+", line.strip())[4] == "-":
                        block = []
                else: block.append(line)
            else: f_out.write(line)
            




with open(in_maf) as f_in:
    for line in f_in:
        if line[0] == "#": f_out.write(line)
        elif line[0] == "\n"
