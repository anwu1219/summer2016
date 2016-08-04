import sys


contentSAT = {}
contentUNSAT = {}
for i in range(301):
    contentSAT[i] = 0
    contentUNSAT[i] = 0
with open(sys.argv[1],'r') as in_file:
    for line in in_file:
        line = line.split()
        if line[-1] == '0':
            contentUNSAT[int(line[1])] += 1
        else:
            contentSAT[int(line[1])] += 1
with open(sys.argv[2], 'w') as out_file:
    for i in range(301):
        out_file.write("%d\t%d\n" %(contentUNSAT[i], contentSAT[i]))
    
