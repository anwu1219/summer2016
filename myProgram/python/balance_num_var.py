import sys
import numpy as np
import random

occurrence = {}
with open(sys.argv[1], 'r') as in_file:
    i = 0
    for line in in_file:
        line = map(int, line.split())
        occurrence[i] = [min(line[0], line[1]), min(line[0], line[1])]
        i += 1

original_file = sys.argv[2]
new_file = sys.argv[3]


content = []
with open(original_file, 'r') as in_file:
    contents = in_file.readlines();
    random.shuffle(contents)
    for line in contents:
        content.append(line.split())
with open(new_file, 'w') as out_file:
    for line in content:
        num_var = int(line[1])
        tar = int(line[-1])
        if occurrence[num_var][tar] != 0:
            out_file.write(" ".join(line) + "\n")
            occurrence[num_var][tar] -= 1

            


    
