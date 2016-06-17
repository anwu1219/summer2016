
import os
import sys


"""
This file is used to obtain training data.
"""
def main():
    original_cnf = sys.argv[1]
    with open(original_cnf, 'r') as in_file: # Read a dimacs file
        in_content = in_file.readlines()

    temp = in_content[1].split()
    n_vars = int(temp[2]) # Get the number of variable


    
    for i in range(n_vars+1)[1:]:
        
        new_dimacs_name_pos = original_cnf.split("/")[-1].split(".")[0]+"-" + str(i) + ".dimacs"
        write_file(i, new_dimacs_name_pos, in_content)
        new_dimacs_name_neg = original_cnf.split("/")[-1].split(".")[0]+"-" + str(-i) + ".dimacs"
        write_file(-i, new_dimacs_name_neg, in_content)




def write_file(lit, new_dimacs_name, in_content):
    deleted_clause = 0
    new_dimacs = [in_content[0],[]]
    for line in in_content[2:]:
        int_lst = map(int, line.split())
        if lit not in int_lst:
            if -lit in int_lst:
                int_lst.remove(-lit)
            new_dimacs.append(" ".join(map(str, int_lst)))
        else:
            deleted_clause += 1
    info = in_content[1].split()
    info[2] = str(int(info[2]) - 1)
    info[3] = str(int(info[3]) - deleted_clause)
    new_dimacs[1] = " ".join(info) # update the number of clauses
    with open(new_dimacs_name, 'w') as out_file:
        out_file.write(new_dimacs[0]) # The first line has change line itself
        out_file.write(new_dimacs[1] + "\n")
        for line in new_dimacs[2:]:
            line = " ".join(update_line(line, abs(lit)))
            out_file.write(line + "\n")
    return


def update_line(line, var):
    linel = map(int, line.split())
    for i in range(len(linel)):
        if abs(linel[i]) > var:
            sign = linel[i] / abs(linel[i])
            linel[i] = sign * (abs(linel[i]) - 1)
    return map(str, linel)

if __name__ == "__main__":
    main()
