import sys

with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()

s = set([])

with open(sys.argv[2], 'w') as out_file:
    for line in content:
        new_line = line.split()
        if new_line[0] not in s and "-" in new_line[0]:
            out_file.write(" ".join(line.split()[:-1])+ "\n")
            s.add(new_line[0])

