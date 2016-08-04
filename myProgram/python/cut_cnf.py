import sys

with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()
with open(sys.argv[1], 'w') as out_file:
    for line in content:
        if len(line.split()) != 1:
            out_file.write(line)
