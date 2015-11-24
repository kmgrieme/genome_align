#!/usr/bin/env python
import sys

script, genome, rev_genome = sys.argv
chr_complement = dict()

rev_complement = {"A":"T", "C":"G", "G":"C", "T":"A",
                  "a":"t", "c":"g", "g":"c", "t":"a"}
chr_names_ordered = []

with open(genome) as f:
    for line in f:
        line = line.strip()
        if line[0] == ">":
            current_chr = line
            chr_names_ordered.append(current_chr)
            chr_complement[current_chr] = []
            continue
        for letter in line:
            chr_complement[current_chr].append(rev_complement[letter])

output = open(rev_genome, "w")

for name in chr_names_ordered:
    new_name = name + ".revcomp"
    complement = list(reversed(chr_complement[name]))
    output.write(new_name)
    output.write("\n")
    for x in range(0, len(complement), 50):
        output.write(''.join(complement[x:x+50]))
        output.write("\n")
    output.write(''.join(complement[x+50:]))

output.close()
