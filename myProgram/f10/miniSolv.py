
import os
import sys
import shutil
import subprocess
# Takes in a dimacs file and generates a solution file and a solver status file
def main():
        out_name = sys.argv[1].split('.')[0]+'.txt'
        if not os.path.isfile(out_name):
                out = open(out_name,'w')
                subprocess.call(["/home/anwu/minisat/minisat",sys.argv[1], sys.argv[1].split('.')[0]+'Sol.txt'], stdout=out)
                out.close()
if __name__ == "__main__":
    main()
