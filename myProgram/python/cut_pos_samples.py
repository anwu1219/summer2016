import sys
import os
import random

s = set()
with open(sys.argv[2], 'r') as in_file:
    for line in in_file:
        s.add(line.split()[0].split("_")[0][1:])


out_file = open("cut_" + sys.argv[1], "w")
with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()
    random.shuffle(content)
    for line in content:
        if line.split()[0].split("_")[0][1:] not in s:
            out_file.write(line)
            s.add(line.split()[0].split("_")[0][1:])
         
