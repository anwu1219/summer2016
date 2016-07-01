import sys
import random

trainset = open(sys.argv[2], 'w')
testset = open(sys.argv[3], 'w')
with open(sys.argv[1], 'r') as in_file:
    for line in in_file:
        if random.randint(0,4) == 1:
            testset.write(line)
        else:
            trainset.write(line)
trainset.close()
testset.close()
