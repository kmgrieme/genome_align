#!/usr/bin/python
import sys

f = open("Mouse.ChrO.fa","r")
lineno = 0
data = ""
for line in f:
    lineno = lineno + 1
    if lineno > 1:
        data = data + line.rstrip("\n")
f.close()

data = data.upper()

fo = open("ol195.fq", "wb")

lendata = len(data)

for x in range(0, (lendata-200)/5+1):
    i = x * 5
    header = "@window" + str(x+1) + "\n"
    fo.write(header)
    fo.write(data[i:i+200])
    fo.write("\n+\n")
    for y in range(0, 200):
        fo.write("~")
    fo.write("\n")

header = "@window" + str(x+2) + "\n"
fo.write(header)
lastwin = data[(x+1)*5:]
fo.write(lastwin)
fo.write("\n+\n")
lastwinlen = len(lastwin)
for y in range(0, lastwinlen):
    fo.write("~")
fo.write("\n")

fo.close()

print x+2
