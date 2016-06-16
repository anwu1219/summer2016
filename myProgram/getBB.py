
import os
import sys
import shutil
import subprocess
import glob
import timeit

"""
This file is used to obtain training data.
"""
def main():
    start_all = timeit.default_timer()
    original_cnf = sys.argv[1]
    print original_cnf
    with open(original_cnf, 'r') as in_file:
        in_content = in_file.readlines()
    while in_content[0][0] == 'c':
        del in_content[0]
        
    temp = in_content[0].split()
    n_vars = int(temp[2])
    temp[3] = str(int(temp[3])+1)+"\n" #changing the number of clauses
    in_content[0] = " ".join(temp)
    
    for i in range(n_vars+1)[1:]:
        print str(i) + ":",
        cnf_name_pos = original_cnf.split("/")[-1].split(".")[0]+"-" + str(i) + ".dimacs"
        cnf_name_neg = original_cnf.split("/")[-1].split(".")[0]+"--" + str(i) + ".dimacs"
        sat_pos = True
        sat_neg = True
        with open(cnf_name_pos, 'w') as out_file:
            for line in in_content:
                out_file.write(line)
            out_file.write(str(i) + " 0") #adding a unit clause to force this variable to be true
        out = open("temp.dimacs", 'w')
        start = timeit.default_timer()
        subprocess.call(["/Users/anwu/desktop/research/minisatN",cnf_name_pos], stdout=out) 
        # AW This line needs to be changed
        end = timeit.default_timer()
        out.close()
        if "UNSAT" in open("temp.dimacs").read():
            sat_pos = False
        time1 = end-start
        os.remove(cnf_name_pos)
        with open(cnf_name_neg, 'w') as out_file:
            for line in in_content:
                out_file.write(line)
            out_file.write(str(-i) + " 0") #adding a unit clause to force it to be false
        out = open("temp.dimacs", 'w')
        start = timeit.default_timer()
        subprocess.call(["/Users/anwu/desktop/research/minisatN",cnf_name_neg], stdout=out)
        # AW This line needs to be changed
        end = timeit.default_timer()
        out.close()
        if "UNSAT" in open("temp.dimacs").read():
            sat_neg = False
        time2 = end-start
        #different calcualtion methods under difference circumstances.
        if not sat_pos and not sat_neg:
            extime1 = time1 + time2
            extime2 = time1 + time2
            extime3 = time1 + time2
        elif sat_pos and not sat_neg:
            extime1 = time1 + 0.5 * time2
            extime2 = time1 + time2
            extime3 = time1 + time2
        elif not sat_pos and sat_neg:
            extime1 = 0.5 * time1 + time2
            extime2 = time1 + time2
            extime3 = time1 + time2
        else:
            extime1 = 0.5 * (time1 + time2)
            extime2 = max([time1, time2])
            extime3 = time1 + time2
        print (str(time1) + "," + str(time2) + "," + str(sat_pos) + "," + str(sat_neg) + "," +
              str(extime1) + "," + str(extime2) + "," + str(extime3))
        os.remove(cnf_name_neg)

if __name__ == "__main__":
    main()
