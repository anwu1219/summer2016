
import os
import sys
import shutil
import subprocess
# Takes in a dimacs file and generates a solution file and a solver status file
def main():
        out_name = sys.argv[1].split('.')[0]+'.txt'
        if not os.path.isfile(out_name) or is_indet(out_name):
                out = open(sys.argv[1].split('.')[0]+'Log.txt','w')
                subprocess.call(["/home/anwu/minisat/core/minisat",sys.argv[1], out_name], stdout=out)
                out.close()

def is_indet(out_name):
        with open(out_name, "r") as in_file:
                content = in_file.readlines()
                return len(content) == 0 or "INDET" in content[0]
                        


if __name__ == "__main__":
    main()

