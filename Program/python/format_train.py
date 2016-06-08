import numpy as np
import sys

FORMULA_LENGTH = 300
def main():
    """
    This file is used for constructing the training set for the rank model. The
    function takes in two parameters, one from the "testFeatures" folder, one to
    write to.
    """    
    in_file = open(sys.argv[1])
    content = in_file.readlines()
    in_file.close()
    out = open(sys.argv[2], 'w')
    num_formulas = len(content)/FORMULA_LENGTH
    n = 0
    while n < num_formulas:
        write(content, n, out)
        n += 1
    out.close()
    
def write(content, n, out):
    X = []
    Y = []
    for i in range(FORMULA_LENGTH):
        line = content[n * FORMULA_LENGTH + i].split(",")
        X.append(line[:-4])
        Y.append(line[-4])
    Y = np.array(Y).argsort().argsort() # transforms a given list into rank
    for i in range(len(Y)):
        out.write("{} qid:{}".format(Y[i]+1, n+1))
        for j in range(len(X[i])):
            out.write(" {}:{}".format(j+1, X[i][j]))
            if j == len(X[i]) -1:
                out.write("\n")
            
    
    
if __name__ == "__main__":
    main()