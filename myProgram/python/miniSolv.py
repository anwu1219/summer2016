
import os
import sys
import shutil
import subprocess
# Takes in a dimacs file and generates a solution file and a solver status file
def main():
        action = sys.argv[1]
        if action == '-s': # Solve a formula if it is not solved
                in_name = sys.argv[2]
                out_name = in_name.split('.')[0]+'.sol'
                if not os.path.isfile(out_name) or is_indet(out_name):
                        out = open(in_name.split('.')[0]+'.log','w')
                        subprocess.call(["/home/anwu/minisat/core/minisat", in_name, out_name], stdout=out)
                        out.close()
                else:   
                        print "This formula is already solved."
        elif action == '-ml': # Solve a formula if it is not solved
                in_name = sys.argv[2]
                if len(sys.argv) == 4:
                        out_name = sys.argv[3] + '.sol'
                        out = open(sys.argv[3] + '.log', 'w')
                else:
                        out_name = in_name.split('.')[0]+'.sol'
                        out = open(in_name.split('.')[0]+'.log','w')
                subprocess.call(["/home/anwu/minisatOML/core/minisat", in_name, out_name], stdout=out)
                out.close()
        elif action == '-m': # Give another solution of a solved SAT formula 
                times = int(sys.argv[2])
                in_name = sys.argv[3]
                out_name = in_name.split('.')[0]+'.osol'
                if not os.path.isfile(out_name) or is_sat(out_name):
                        i = 1
                        add_line(in_name, out_name)
                        while i <= times:
                                out_name = out_name.split('.')[0].split('~')[0] + "~" + str(i) + '.sol'
                                out = open(out_name.split('.')[0]+'.log','w')
                                subprocess.call(["/home/anwu/minisat/core/minisat", in_name.split('.')[0] + '~temp.dimacs', out_name], stdout=out)
                                out.close()
                                if (os.path.isfile(out_name) and is_sat(out_name)): # If Solved
                                        add_line(in_name.split('.')[0] + '~temp.dimacs', out_name)
                                        i += 1;
                                else:
                                        break;
                        os.remove(in_name.split('.')[0] + '~temp.dimacs')
        elif action == "-c": # Generates .ulit files for a formula.
                if sys.argv[2] == '-v':
                        remove = False
                        in_name = sys.argv[3]
                else:
                        remove = True
                        in_name = sys.argv[2]
                out = open(in_name.split('.')[0]+'.log','w')
                subprocess.call(["/home/anwu/minisatP/core/minisat", in_name], stdout=out)
                out.close()
                if remove:
                        os.remove(in_name.split('.')[0]+'.log')
        else:
                print "Please enter flags -s/-m/-c"



def add_line(in_name, out_name):
        """
        add the reverse of a previous solution to the formula so that solving it generates a new solution
        """
        content = []
        with open(in_name, 'r') as in_file:
                content = in_file.readlines()
        i = 0
        while content[i][0] != 'p':
                i += 1
        content[i] = content[i].split()
        content[i][3] = str(int(content[i][3]) + 1)
        content[i] = " ".join(content[i]) + "\n"
        with open(out_name, 'r') as in_file:
                old_sol = map(int, in_file.readlines()[1].split())
                for i in range(len(old_sol)):
                        old_sol[i] = -old_sol[i]
                content.append(" ".join(map(str, old_sol)) + "\n")
        with open(in_name.split('.')[0].split('~')[0] + '~temp.dimacs', 'w') as out_file:
                for line in content:
                        out_file.write(line)

def is_sat(out_name):
        """                                                                                                                                       
        Return true if the .sol file is not empty or does not contain "INDET" or "UNSAT"                                                                                 
        """
        with open(out_name, "r") as in_file:
                content = in_file.readlines()
                return len(content) != 0 and ("INDET" not in content[0]) and ("UNSAT" not in content[0])





def is_indet(out_name):
        """
        Return true if the .sol file is empty or contains "INDET"
        """
        with open(out_name, "r") as in_file:
                content = in_file.readlines()
                return len(content) == 0 or "INDET" in content[0]
                        


if __name__ == "__main__":
    main()

