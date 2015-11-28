#!/usr/bin/env python

import sys

script, genome_file = sys.argv

genome = open(genome_file)

for line in genome:
    if line[0] == ">":
        file_name = line[1:].strip() + ".fa"
        working_file = open(file_name, "w")
    working_file.write(line)

working_file.close()
genome.close()
