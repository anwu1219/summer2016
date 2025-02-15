from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
import sys
from sklearn.preprocessing import PolynomialFeatures

def search_for_best_features(X, X_test, X_val, Y, Y_test, Y_val, clf):
	new_X = X[:, 0:1]
	new_X_test = X_test[:, 0:1]
	new_X_val = X_val[:, 0:1]
	#print new_X
	clf.fit(new_X, Y)
	last_score = clf.score(new_X_test, Y_test)
	for i in range(len(X[0])):
		new_X1 = np.append(new_X, X[:, i : i + 1], axis=1)
		new_X_test1 = np.append(new_X_test, X_test[:, i : i + 1], axis=1)
		new_X_val1 = np.append(new_X_val, X_val[:, i : i + 1], axis=1)
		current_score = clf.fit(new_X1, Y).score(new_X_test1, Y_test)
		if (current_score > last_score):
			new_X = new_X1
			new_X_test = new_X_test1
			new_X_val = new_X_val1
			last_score = current_score
        clf.fit(new_X, Y)
        print "Train:", clf.score(new_X, Y)
        print "Test:", clf.score(new_X_val, Y_val)


SAT_FILE_NAME = sys.argv[1] # used to build the models
UNSAT_FILE_NAME = sys.argv[2]
from random import shuffle

X = []
Y = []
X_test = []
Y_test = []
data = []
with open(SAT_FILE_NAME, 'r') as in_file:
	data_set = in_file.readlines()
	for line in data_set:
		line =line.split()[1:] # skip the formula identifier
		data.append(map(float, line))

with open(UNSAT_FILE_NAME, 'r') as in_file:
        data_set = in_file.readlines()
        for line in data_set:
                line =line.split()[1:] # skip the formula identifier                                                        
                data.append(map(float, line))

np.random.shuffle(data)
train_index = int(0.8 * len(data))

for line in data[:train_index]:
        X.append(line[:-1])
        Y.append(line[-1])
for line in data[train_index:]:
        X_test.append(line[:-1])
        Y_test.append(line[-1])

#scaler = preprocessing.StandardScaler().fit(X)
#X = scaler.transform(X)
#X_test = scaler.transform(X_test)
print np.sum(Y), "negative samples out of", len(Y), "in train set"
print np.sum(Y_test), "negative samples out of", len(Y_test), "in test set"
#poly = PolynomialFeatures(2)
#poly.fit_transform(X)
#poly.fit_transform(X_test)
a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
clf1 = RandomForestClassifier(n_estimators = 400,  n_jobs = -1)
#clf1 = DecisionTreeClassifier()
#clf1 = KNeighborsClassifier(n_neighbors = 39, n_jobs = -1, weights = 'distance')
#clf1 = LogisticRegression()

#clf1 = LinearSVC()
# print "Learning..."
clf1.fit(X, Y)
print "Feature importance:", clf1.feature_importances_ 
print "Train score:",clf1.score(X, Y)
print "Test score:", clf1.score(X_test, Y_test)
# #predict2 = clf2.score(X_test, Y_test)
# 	print predict1
# except ValueError:
# 	print "fail"

#print search_for_best_features(np.array(X), np.array(X_test), np.array(X_val), Y, Y_test, Y_val, clf1)


