import sys
import os
import random

"""
Takes in a data file, and randomly split it into a testset and a trainset
"""

if random.randint(0,4) == 1:
    os.rename("./" + sys.argv[1], "./testset/" + sys.argv[1])   
else:
    os.rename("./" + sys.argv[1], "./trainset/" + sys.argv[1])

