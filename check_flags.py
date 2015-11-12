#!usr/bin/env python
import sys
script, sam_file = sys.argv

flag_dict = dict()

with open(sam_file, "r") as f:
    line_num = 0
    for line in f:
        print("Processing line %s" % line_num, end="\r")
        if line[0] == "@":
            continue
        flag = int(line.split("\t")[1])
        try:
            flag_dict[flag] += 1
        except KeyError:
            flag_dict[flag] = 1
        line_num += 1

print("\nDone processing SAM file. Writing flag information.")
flags = list(flag_dict.keys())
flags.sort()

with open("%s_flag_list.txt" % sam_file[:-4], "w") as f:
    for key in flags:
        f.write("Flag %s: %s\n" % (key, flag_dict[key]))
