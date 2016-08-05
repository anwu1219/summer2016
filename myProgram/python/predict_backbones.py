import os
import sys
import shutil
import subprocess
# Takes in a dimacs file and generates a solution file and a solver status file                                                                               
in_name = sys.argv[1]
out = open(in_name.split('.')[0]+'.log','w')
subprocess.call(["/home/anwu/Summer2016/myProgram/C++/predictBackbone.out", in_name], stdout=out)
out.close()
