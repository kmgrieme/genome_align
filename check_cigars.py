#!/usr/bin/env python
import sys

script, sam_file = sys.argv

incorr_count = 0
line_count = 0

sam = open(sam_file)

for line in sam:
    if line[0] == "@": continue
    cigar = line.split('\t')[5]
    if cigar[-1] == "S" and "S" not in cigar[:-1]:
        incorr_count += 1
    line_count += 1

sam.close()

print("Cigars total: %s" % line_count)
print("Cigars incorrect: %s" % incorr_count)
print("Percent incorrect: %s%" % ((incorr_count/line_count)*100))
