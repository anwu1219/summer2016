import sys

line = []
with open(sys.argv[1], 'r') as in_file:
    content = in_file.readlines()
    if "SAT" in content[-1]:
        line.append(sys.argv[1].split('.')[0])
        line.append(content[-9].split()[2])
        line.append(content[-8].split()[2])
        line.append(content[-7].split()[2])
        line.append(content[-6].split()[2])    
        line.append(content[-3].split()[3])
        line.append(content[-1].split()[0])
        with open(sys.argv[2], 'a') as out_file:
            out_file.write(" ".join(line) + "\n")
    
