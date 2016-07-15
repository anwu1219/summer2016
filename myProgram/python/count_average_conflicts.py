import sys

s = 0
count = 0
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        s += float(line.split()[2])
        count += 1
print s / count
