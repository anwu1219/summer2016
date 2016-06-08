import sys
from sklearn import preprocessing
import numpy as np
import math
def main():
    Y_NAME = sys.argv[1]
    Y_file = open(Y_NAME, 'r')
    content = Y_file.readlines()
    X_NAME = content[0].split("/")[-1].split(".")[0] + ".txt"
    Y = content[1:]
    X_file = open(X_NAME)
    X = X_file.readlines()
    X_file.close()
    Y_file.close()
    
    for i in range(len(X)):
        X[i] = X[i].replace("\n","").split(":")[1].split(",")[:-1]
    
    T = np.empty([len(Y), 3])
    for i in range(len(Y)):
        Y[i] = Y[i].split(":")[1].split(",")
        T[i, 0] = math.log1p(float(Y[i][-3]))
        T[i, 1] = math.log1p(float(Y[i][-2]))
        T[i, 2] = math.log1p(float(Y[i][-1]))
    #T = preprocessing.scale(T)
    #binarizer = preprocessing.Binarizer()
    #threshold = np.percentile(T, 40, axis = 0)
    #T_columns = []
    #for i in range(3):
        #T_columns.append(T[:,i])
        #binarizer.set_params(threshold = threshold[i])
        #T_columns[i] = binarizer.transform(T_columns[i].reshape(1,300))
    
    for i in range(len(X)):
        for j in range(len(X[i])):
            sys.stdout.write(str(X[i][j]) + ",")
        for k in range(3):
            sys.stdout.write(str(T[i,k]) + ",")
            #sys.stdout.write(str(T_columns[k][0,i]) + ",")
        print
if __name__ == "__main__":
    main()