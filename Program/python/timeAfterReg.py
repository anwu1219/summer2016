import sys
import subprocess
import timeit
import random
import os
"""
This is a helper file to the checkBranch.py file.
"""
def process(original_cnf, var):    # AW Input example: /testSet2/test2_ksat-1.dimacs
    """
    calculates the raw running time (giving whether SAT or UNSAT) after branching
    on the given variable.
    """
    
    time,sat = minisat(original_cnf)
    print time, var
    with open(original_cnf, 'r') as in_file:
        in_content = in_file.readlines()
    while in_content[0][0] == 'c':
        del in_content[0]        # AW Delete the first line of the dimacs file
    
    temp = in_content[0].split()   
    n_vars = int(temp[2]) # AW Get the number of variable
    temp[3] = str(int(temp[3])+1)+"\n" # AW Add one clause 
    in_content[0] = " ".join(temp)
    var_to_test = range(n_vars+1)[1:] # Starting from 1

    for i in var_to_test: # Try to start with each variable 
        cnf_name = original_cnf.split("/")[-1].split(".")[0]+"-" + str(i) + ".dimacs"
        with open(cnf_name, 'w') as out_file: # Add Pos unit clause
            for line in in_content:
                out_file.write(line)
            out_file.write(str(i) + " 0")
        time, sat = minisat(cnf_name)
        print i, time, sat,
        os.remove(cnf_name)
        with open(cnf_name, 'w') as out_file: # Add Neg unit clause
            for line in in_content:
                out_file.write(line)
            out_file.write("-" + str(i) + " 0")
        time, sat = minisat(cnf_name)
        print time, sat
        os.remove(cnf_name)
        
def minisat(cnf):
    out = open("junk.txt","w")
    sat = True
    start = timeit.default_timer()
    subprocess.call(["/Users/anwu/desktop/research/minisatN", cnf], stdout = out)
    # AW This line needs to be changed
    end = timeit.default_timer()
    if "UNSAT" in open("junk.txt").read():
        sat = False
    out.close()
    return end-start, sat
if __name__ == "__main__":
    main()
