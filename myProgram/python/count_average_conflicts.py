import sys
import numpy as np

lst = []
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        lst.append(float(line.split()[2]))
print "mean", np.mean(lst)
print "median", np.median(lst)
