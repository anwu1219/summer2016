import sys 
import shutil
import random

r = random.randint(0,4)
print sys.argv[1]
if r == 0:
    shutil.move(sys.argv[1], "testset/" + sys.argv[1])
else:
    shutil.move(sys.argv[1], "trainset/" + sys.argv[1])
