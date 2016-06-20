from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2



TRAIN_FILE_NAME = "train_set.txt" # used to build the models
TEST_FILE_NAME = "test_set.txt"
from random import shuffle

def main():
    X = []
    Y = []
	with open("train_set.txt", 'r') as in_file:
		train_set = in_file.readlines()
		for line in train_set:
			X.append(line[:-1])
			Y.append(line[-1])

	X_test = []
	Y_test = []
	with open("test_set.txt", 'r') as in_file:
		train_set = in_file.readlines()
		for line in train_set:
			X_test.append(line[:-1])
			Y_test.append(line[-1])


    a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
    clf1 = RandomForestRegressor(n_estimators = 400)
    #clf2 = RidgeCV(alphas = a[2:5])
    clf1.fit(X[:], Y)
    clf2.fit(X[:], Y)
    predict1 = clf1.score(X_test, Y_test)
    #predict2 = clf2.score(X_test, Y_test)
    print predict1#, predict2
  

  if __name__ == "__main__":
    main()
