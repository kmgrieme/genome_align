#!usr/bin/env python
import sys

if len(sys.argv) != 5:
    print("Please run in the format script, input genome, destination, index jump, read length.")
    quit()

script, in_file, out_file, index, length = sys.argv
print("Reading data from %s." % in_file)

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
    progress_str = "Processing chromosome %s, file line %s"
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
        print(progress_str % (chr_names[chr_num], line_num), end="\r")
        '''
        if line_num % 50000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()
        '''

print("\n\n%s chromosomes read. Beginning read windows." % (chr_num+1))
print("Writing to file %s.\n" % out_file)
reads = open(out_file, "w")
header_string = "@%s_%s_L%s_win%s\n" # chromosome name, index, L+len, window

progress_str = "Creating read %s for chromosome %s (total: %s)"
total_reads = 0

for chr_num in range(0, len(data), 1):
    print("Joining strings for chromosome %s." % chr_names[chr_num])
    chromosome = "".join(data[chr_num])
    print("Writing reads for %s." % chr_names[chr_num])
    chromosome = chromosome.upper()
    for x in range(0, (len(chromosome)-length)//index+1, 1):
      ## creates length reads every index
      ## i: index in the sequence; x+1: window number
        i = x * index
        total_reads += 1
        reads.write(header_string % (chr_names[chr_num], i, length, x+1))
        reads.write(chromosome[i:i+length])
        reads.write("\n+\n")
        reads.write("~"*length) # read quality for fastq format
        reads.write("\n")
        print(progress_str % (x+1, chr_names[chr_num], total_reads), end="\r")
        '''
        if x % 50000 == 0: # to check progress
            print(".",end="")
            sys.stdout.flush()
        '''
    last_window = chromosome[(x+1)*index:]
    reads.write(header_string % (chr_names[chr_num], (x+1)*index, len(last_window), x+2))
    reads.write(last_window)
    reads.write("\n+\n")
    reads.write("~"*len(last_window))
    reads.write("\n")
    total_reads += 1
    print("%s reads written for %s; %s reads total." % (x+2, chr_names[chr_num], total_reads))

print("\nRead generation complete. Closing write file.")
reads.close()
