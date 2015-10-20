#! usr/bin/env python
import sys

script, in_file, out_file = sys.argv
print("Reading data from %s" % in_file)

## The original script added each line of the file to a string.
## This begins a list for every chromosome in the file and appends each line to it.
## Only makes a string out of the chromosome when creating reads.
## Speeds the program up significantly since python isn't making new strings constantly.
## Print statements for python 3 but without them & range > xrange it should run in python 2

with open(in_file, "r") as f:
    lineno = 0
    chr_num = 0
    for line in f:
        if lineno == 0:
            data = [[]]
            print("Beginning reads of chromosome %s" % (chr_num+1))
        elif line[0] == ">":
            chr_num += 1
            data.append([])
            print("\nBeginning reads of chromosome %s" % (chr_num+1))
        else:
            data[chr_num].append(line.rstrip())
        lineno += 1
        if lineno % 10000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()

print("\n%s chromosomes read. Beginning read windows." % (chr_num+1))

reads = open(out_file, "w")

for chr_num in range(0, len(data), 1):
    print("Joining strings.")
    chromosome = "".join(data[chr_num])
    print("Writing reads for %s." % (chr_num+1))
    lendata = len(chromosome)
    chromosome = chromosome.upper()
    for x in range(0, (lendata-200)//5+1, 1): # not sure why ling used these numbers
        i = x * 5
        header = "@window %s chr%s\n" % (x+1, chr_num+1)
        reads.write(header)
        reads.write(chromosome[i:i+200])
        reads.write("\n+\n")
        reads.write("~"*200)
        reads.write("\n")
        if x % 50000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()
    print()
    header = "@window %s chr%s\n" % (x+2, chr_num+1)
    reads.write(header)
    last_window = chromosome[(x+1)*5:]
    reads.write(last_window)
    reads.write("\n+\n")
    reads.write("~"*len(last_window))
    reads.write("\n")

print("Read generation complete. Closing write file.")
reads.close()
