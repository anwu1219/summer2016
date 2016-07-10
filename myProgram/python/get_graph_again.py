import graph as gr
import sys
import os

content = []
out_file = sys.argv[2]
with open(sys.argv[1], "r") as in_file:
    for line in in_file:
        line = line.split()
        if os.path.isfile(line[0] + ".dimacs"):
            gr.main(line[0] + ".dimacs", int(line[-1]), out_file)
