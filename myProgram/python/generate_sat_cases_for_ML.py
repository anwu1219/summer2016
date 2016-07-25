import sys
import random_ksat as rk

num_vars = int(sys.argv[1])
num_clauses = int(num_vars * 4.26)
loop_time = int(sys.argv[2])
for i in range(1, loop_time + 1):
        output  = rk.generate_instance(num_clauses, num_vars, 3, True)
        f = open(sys.argv[3] + "-" + str(i)+ ".dimacs","w")
        f.write(output)
        f.close()

    




