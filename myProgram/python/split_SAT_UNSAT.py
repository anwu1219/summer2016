import sys
import os

with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()
    if "UNSAT" in content[0]:
        os.rename("./" + sys.argv[1].split('.')[0] + ".cnf", "./UNSAT/" + sys.argv[1].split('.')[0] + ".cnf")
#        os.rename("./" + sys.argv[1].split()[0] + ".txt", "./UNSAT" + sys.argv[1].split()[0] + ".txt")
        os.rename("./" + sys.argv[1].split('.')[0] + ".log", "./UNSAT/" + sys.argv[1].split('.')[0] + ".log")
        os.rename("./" + sys.argv[1].split('.')[0] + ".sol", "./UNSAT/" + sys.argv[1].split('.')[0] + ".sol")

