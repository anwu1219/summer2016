"""
Takes in a known UNSAT dimacs file and generates a .sol file that contains "UNSAT"
"""

import sys

with open(sys.argv[1].split('.')[0]+'.sol', 'w') as out_file:
    out_file.write('UNSAT\n')
