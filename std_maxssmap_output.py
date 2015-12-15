#!/usr/bin/env python

import sys
from re import sub

script, sam_file, sam_fix = sys.argv

line_count = 0

with open(sam_file) as f_in:
    with open(sam_fix, "w") as f_out:
        for line in f_in:
            if "Character" in line:
                continue
            new_line = sub(r">", "", line)
            if new_line[0] == "@":
                line_count += 1
                if line_count > 2:
                    new_line = new_line[1:]
            f_out.write(new_line)
