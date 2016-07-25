import sys

file_1 = sys.argv[1]
file_2 = sys.argv[2]
content = []
with open(file_1, 'r') as in_file:
    for line in in_file:
        content.append(line)
with open(file_2, 'r') as in_file:
    for line in in_file:
        content.append(line)
with open(sys.argv[3], 'w') as out_file:
    for line in content:
        if 'n' not in line.split()[1:]:
            out_file.write(line)


