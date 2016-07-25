from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
import sys


def search_for_best_features(X, X_test, Y, Y_test, clf):
	new_X = X[:, 0:1]
	new_X_test = X_test[:, 0:1]
#	new_X_val = X_val[:, 0:1]
	print new_X
	clf.fit(new_X, Y)
	last_score = clf.score(new_X_test, Y_test)
	for i in range(len(X[0])):
		print last_score
		new_X1 = np.append(new_X, X[:, i : i + 1], axis=1)
		new_X_test1 = np.append(new_X_test, X_test[:, i : i + 1], axis=1)
#		new_X_val1 = np.append(new_X_val, X_val[:, i : i + 1], axis=1)
		current_score = clf.fit(new_X1, Y).score(new_X_test1, Y_test)
		if (current_score > last_score):
			new_X = new_X1
			new_X_test = new_X_test1
#			new_X_val = new_X_val1
			last_score = current_score
	return last_score


TRAIN_FILE_NAME = sys.argv[1] # used to build the models
# TEST_FILE_NAME = sys.argv[2]
from random import shuffle

X = []
Y = []
X_test = []
Y_test = []
X_val = []
Y_val = []

#with open(TRAIN_FILE_NAME, 'r') as in_file:
#	train_set = in_file.readlines()
#	for line in train_set:
#		line = line.split()[2:12] + line.split()[13:] # skip the formula identifier
#		try:
#			X.append(map(float, line[:-1])) 
#			Y.append(float(line[-1]))
#		except ValueError:
#			print line

with open(TRAIN_FILE_NAME, 'r') as in_file:
	train_set = in_file.readlines()
	for line in train_set[:80]:
		line = line.split()[2:12] + line.split()[13:]
		try:
			X.append(map(float, line[:-1]))
			Y.append(float(line[-1]))
		except ValueError:
			print line
	for line in train_set[80:]:
		line = line.split()[2:12] + line.split()[13:]
		try:
			X_test.append(map(float, line[:-1]))
			Y_test.append(float(line[-1]))
		except ValueError:
			print line
#	for line in train_set[18000:]:
#		line = line.split()[2:12] + line.split()[13:]
#		try:
#			X_val.append(map(float, line[:-1]))
#			Y_val.append(float(line[-1]))
#		except ValueError:
#			print line

#scaler = preprocessing.StandardScaler().fit(X)
#X = scaler.transform(X)
shuffle(X)
#X_test = scaler.transform(X_test)
print np.sum(Y_test), "negative samples out of", len(Y_test)
print np.sum(Y_val), "negative samples out of", len(Y_val)

a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
#clf1 = RandomForestClassifier(n_estimators = 50, n_jobs = -1)
#clf1 = KNeighborsClassifier(n_neighbors = 39, n_jobs = -1, weights = 'distance')
clf1 = LogisticRegression()
# #clf1 = LinearSVC()
# print "Learning..."
# clf1.fit(X, Y)
# #clf2.fit(X[:], Y)
# try:
# 	predict1 = clf1.score(X_test, Y_test)
# #predict2 = clf2.score(X_test, Y_test)
# 	print predict1
# except ValueError:
# 	print "fail"

print search_for_best_features(np.array(X), np.array(X_test), Y, Y_test, clf1)


