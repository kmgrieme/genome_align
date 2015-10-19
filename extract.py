#!/usr/bin/python
import re

f = open("newCow.ChrC.fa","r")
lineno = 0
data = ""
for line in f:
    lineno = lineno + 1
    if lineno > 1:
        data = data + line.rstrip("\n")
f.close()

out = open("MSMCowMouseOL195.o754672","r")
fo = open("ol195.maf", "wb")
fo.write("##maf version=1\n")
lno = 0
s = ""
for line in out:
    lno = lno + 1
    if lno > 2 and lno < 789948:
        s = line.rstrip("\n")

        list = s.split("\t")
        flag = list[1]

        position = list[3]

        cigar = list[5]

        read = list[9]
            #print cigar

        if int(flag) != 4:
        # # data = "CCATACTGAACTGACTAAC"
        # # read = "ACTAGAATGGCT"
        # # cigar = "3M1I3M1D5M"
            
            clength = len(cigar)
            index = 0
            begin = 0
            end = 0

        # # #cow
            index1 = int(position) - 1
            seq1 = ""
        # # #mouse
            index2 = 0
            seq2 = ""
            m = 0
            d = 0
            j = 0

            while (index < clength):
                c = cigar[index:index + 1]
                if c == "M" or c == "I" or c == "D":
                   end = index
                   po = cigar[begin:end]
                   po = int(po)
                   begin = index + 1
                   #print po
                   if c == "M":
                        seq1 = seq1 + data[index1 : index1 + po]
                        seq2 = seq2 + read[index2 : index2 + po]
                        index1 = index1 + po
                        index2 = index2 + po
                        m = m + po
                   if c == "I":
                        i = 0
                        while (i < po):
                            seq1 = seq1 + "-"
                            i = i + 1
                        seq2 = seq2 + read[index2 : index2 + po]
                        index2 = index2 + po
                        j = j + po
                   if c == "D":
                        i = 0
                        while (i < po):
                            seq2 = seq2 + "-"
                            i = i + 1
                        seq1 = seq1 + data[index1 : index1 + po]
                        index1 = index1 + po
                        d = d + po
                index = index + 1

            #print seq1
            #print seq2
        # # # print m,j,d,int(position) - 1,index1,index2

            winn = int(list[0][7:]) - 1
            i1 = int(position) - 1
            i2 = winn * 5

        # # # print i1,i2    
        # # # print seq1
        # # # print seq2

            fo.write("a score=0.0\n")
            strand = "s simCow.chrC"
            fo.write(strand.ljust(16))
            strand = str(i1)
            fo.write(strand.rjust(10))
            strand = str(m+d)
            fo.write(strand.rjust(5)+" + ")
            strand = "33408597 "
            fo.write(strand.rjust(10))
            fo.write(seq1)
            fo.write("\n")
            strand = "s simMouse.chrO"
            fo.write(strand.ljust(16))
            strand = str(i2)
            fo.write(strand.rjust(10))
            strand = str(m+j)
            if int(flag) == 0:
                fo.write(strand.rjust(5)+" + ")
            else:
                fo.write(strand.rjust(5)+" - ")
            strand = "3949899 "
            fo.write(strand.rjust(10))
            fo.write(seq2)
            fo.write("\n\n")
fo.close()
out.close()



