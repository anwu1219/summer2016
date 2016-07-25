import sys
import numpy as np

lst = []
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
<<<<<<< HEAD
        lst.append(float(line.split()[1]) - 1)
print "mean number of restart", np.mean(lst)
print "median number of restart", np.median(lst)
=======
        lst.append(float(line.split()[2]))
print "mean", np.mean(lst)
print "median", np.median(lst)
>>>>>>> 4c806fe2d4eea75f88b3ccff6200a49df051cb0b
