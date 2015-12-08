#!/usr/bin/env python

import sys

script, in_genome, dest = sys.argv

with open(in_genome) as f_in:
    with open(dest, "w") as f_out:
        for line in f_in:
            if line[0] == ">": f_out.write(line)
            else: f_out.write(line.upper())
