import sys
import numpy as np

SATlst = []
UNSATlst = []
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        if line.split()[-1] == "SATISFIABLE":
            SATlst.append(float(line.split()[2]))
        else:
            UNSATlst.append(float(line.split()[2]))
print "mean SAT runtime", np.mean(SATlst)
print "median SAT runtime", np.median(SATlst)
print "mean UNSAT runtime", np.mean(UNSATlst)
print "median UNSAT runtime", np.median(UNSATlst)

