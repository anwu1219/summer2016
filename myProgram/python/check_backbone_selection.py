import sys
import os

with open(sys.argv[1], 'r') as in_file:
    content = map(int, in_file.readlines()[2:])
num_backbone = 0
wrong = 0
if len(content) == 1:
    for ele in content:
        if os.path.isfile("UNSAT/u" + sys.argv[1].split('.')[0] + "_" + str(ele) + ".dimacs") or os.path.isfile("UNSAT/u" + sys.argv[1].split('.')[0] + "_" + str(-ele) + ".dimacs"):
            num_backbone += 1
            if os.path.isfile("UNSAT/u" + sys.argv[1].split('.')[0] + "_" + str(ele) + ".dimacs"):
                wrong += 1
    print wrong, num_backbone
                          
