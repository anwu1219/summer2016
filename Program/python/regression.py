
from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
import sys
import glob

"""
Unlike analyze.py, this file uses machine learning models and computes the best
branching varaible for each formula in the test folder. For each file, it prints
out the file name, the best branching variable for random forest and the best 
for ridge.
"""

FILE_NAME = "txt/featuresAll.txt" # used to build the models
TEST_FOLDER = sys.argv[1] # test solver performance
from random import shuffle
def main():
    data_file = open(FILE_NAME)
    content = data_file.readlines()
    data_file.close()
    
    X = []
    Y = [[],[],[]]
    num_features = -1
    for i in range(len(content)):
        X.append([])
        line = content[i][:-2].split(",")
        if num_features == -1:
            num_features = len(line)-3
        for j in range(len(line)):
            if j < num_features:
                X[i].append(float(line[j]))
            else:
                Y[j-num_features].append(float(line[j]))
    a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
    clf1 = RandomForestRegressor(n_estimators = 400)
    clf2 = RidgeCV(alphas = a)
    clf1.fit(X[:], Y[0][:])
    clf2.fit(X[:], Y[0][:])
    
    for TEST_FILE_NAME in glob.glob(TEST_FOLDER+"/*"):
        test_file = open(TEST_FILE_NAME)
        X_test = test_file.readlines()
        test_file.close()
        extract(X_test)    
        predict1 = clf1.predict(X_test)
        predict2 = clf2.predict(X_test)
        print TEST_FILE_NAME, np.argmin(predict1)+1, np.argmin(predict2)+1

def extract(X):
    """
    Transforms data into float representations.
    """
    for i in range(len(X)):
        X[i] = X[i].replace("\n","").split(":")[1].split(",")[:-1]
        for j in range(len(X[i])):
            X[i][j] = float(X[i][j])
if __name__ == "__main__":
    main()
