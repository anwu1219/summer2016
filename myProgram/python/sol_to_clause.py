import sys

s = []
with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()[1].split()[:-1]
    for ele in content:
        s.append(str(ele) + " 0\n")
with open(sys.argv[1].split('.')[0] + '.cnf', 'r') as in_file:
    content = in_file.readlines()
    content = content[:2] + s + content[2:]
with open('temp' + sys.argv[1].split('.')[0] + '.cnf', 'w') as out_file:
    for line in content:
        out_file.write(line)
