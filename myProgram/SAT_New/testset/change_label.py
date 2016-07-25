import sys

content = []
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        line = line.split()
        line[-1] = "1"
        content.append(" ".join(line) + "\n")
with open(sys.argv[1], 'w') as out_file:
    for line in content:
        out_file.write(line)
