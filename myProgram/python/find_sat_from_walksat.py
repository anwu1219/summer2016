import sys
import os

with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()
    if "NOT" in content[-1]:
        os.rename("./" + sys.argv[1].split('.')[0] + ".cnf", "./UNSAT/" + sys.argv[1].split('.')[0] + ".cnf")
        os.rename("./" + sys.argv[1].split('.')[0] + ".log", "./UNSAT/" + sys.argv[1].split('.')[0] + ".log")    
