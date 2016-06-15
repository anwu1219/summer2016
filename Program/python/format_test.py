import numpy as np
import sys

FORMULA_LENGTH = 300 # Each instance is a variable
def main():
    """
    This file is used for constructing the test set for the rank model. The 
    given input should be in the "testFeatures" folder. It prints everything in
    the console.
    """
    in_file = open(sys.argv[1])
    content = in_file.readlines()
    in_file.close()
    for i in range(FORMULA_LENGTH):
        line = content[i].split(":")[-1].split(",")[:-1] # AW split the line, line is the list of each feature
        print "{} qid:{}".format(i+1, sys.argv[2]), # AW What is qid?
        for j in range(len(line)): 
            print "{}:{}".format(j+1, line[j]), # Print out each feature
        print
if __name__ == "__main__":
    main()