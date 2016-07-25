import sys

out_file = open(sys.argv[3], 'w')
with open(sys.argv[1],'r') as in_file:
    for line in in_file:
        line = line.split()
        line[-1] = sys.argv[2]
        out_file.write(" ".join(line) + "\n")
out_file.close()
