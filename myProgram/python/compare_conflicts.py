import sys


content = []
time = []
example = []
SATcount = 0
SATtotal = 0
UNSATcount = 0
UNSATtotal = 0
SATtimebeat = 0
UNSATtimebeat = 0
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        content.append(int(line.split()[2]))
        time.append(float(line.split()[-2]))
        example.append(line.split()[0])
with open(sys.argv[2], 'r') as in_file:
    i = 0
    for line in in_file:
        if line.split()[-1] == 'SATISFIABLE':
            SATtotal += 1
        elif  line.split()[-1] == 'UNSATISFIABLE':
            UNSATtotal += 1
        if float(line.split()[-2]) == time[i]:
            print "wierd", line.split()[0]
        if float(line.split()[-2]) < time[i]:
            if line.split()[-1] == 'SATISFIABLE':
                SATtimebeat += 1
            elif  line.split()[-1] == 'UNSATISFIABLE':
                UNSATtimebeat += 1
        if int(line.split()[2]) < content[i]:
            if line.split()[-1] == 'SATISFIABLE':
                SATcount += 1
            elif  line.split()[-1] == 'UNSATISFIABLE':
                UNSATcount += 1
        i+= 1
print sys.argv[2], "outperforms", sys.argv[1], "in", SATcount, "out of", SATtotal, "SAT examples"
print sys.argv[2], "outperforms", sys.argv[1], "in", UNSATcount, "out of", UNSATtotal, "UNSAT examples"
print "It is highly unlikely, but", sys.argv[2], "outperforms", sys.argv[1], "in terms of time in", SATtimebeat, "out of", SATtotal, "SAT examples"
print "It is highly unlikely, but", sys.argv[2], "outperforms", sys.argv[1], "in terms of time in", UNSATtimebeat, "out of", UNSATtotal, "UNSAT examples"
