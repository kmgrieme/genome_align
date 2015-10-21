#!usr/bin/env python
import sys

script, in_file, out_file = sys.argv
print("Reading data from %s.\n" % in_file)

## The original script added each line of the file to a string.
## This begins a list for every chromosome in the file and appends each line to it.
## Only makes a string out of the chromosome when creating reads.
## Speeds the program up significantly since python isn't making new strings constantly.
## Print statements for python 3 but without them & range > xrange it should run in python 2

with open(in_file, "r") as f:
    line_num = 0
    chr_num = 0
    data = []
    chr_names = []
    for line in f:
      ## if line starts with >, gets sequence name information
        if line[0] == ">":
            name = line[1:].rstrip()
            chr_names.append(name)
            data.append([])
            if line_num != 0:
                chr_num += 1
            print("\nReading %s" % chr_names[chr_num])
      ## pulls each line, strips, appends to array for chromosome
        else:
            data[chr_num].append(line.rstrip())
        line_num += 1
        if line_num % 50000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()

print("\n\n%s chromosomes read. Beginning read windows." % (chr_num+1))
print("Writing to file %s.\n" % out_file)
reads = open(out_file, "w")
header_string = "@%s_%s_l%s_win%s\n" # chromosome name, index, l+len, window

for chr_num in range(0, len(data), 1):
    print("Joining strings.")
    chromosome = "".join(data[chr_num])
    print("Writing reads for %s." % chr_names[chr_num])
    chromosome = chromosome.upper()
    for x in range(0, (len(chromosome)-200)//5+1, 1):
      ## creates 200bp reads every 5bp
      ## i: index in the sequence; x+1: window number
        i = x * 5
        reads.write(header_string % (chr_names[chr_num], i, 200, x+1))
        reads.write(chromosome[i:i+200])
        reads.write("\n+\n")
        reads.write("~"*200) # read quality for fastq format
        reads.write("\n")
        if x % 50000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()
    last_window = chromosome[(x+1)*5:]
    reads.write(header_string % (chr_names[chr_num], (x+1)*5,
                                 len(last_window), x+2))
    reads.write(last_window)
    reads.write("\n+\n")
    reads.write("~"*len(last_window))
    reads.write("\n")
    print("\n%s reads written for %s.\n" % (x+2, chr_names[chr_num]))

print("\nRead generation complete. Closing write file.")
reads.close()
