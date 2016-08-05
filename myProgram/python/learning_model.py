from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV, LogisticRegressionCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
import sys
import random
from sklearn import cross_validation
from sklearn import datasets

TRAIN_FILE_NAME = sys.argv[1] # used to build the models


X = []
Y = []
X_test = []
y_test = []

with open(TRAIN_FILE_NAME, 'r') as in_file:
        data_set = in_file.readlines()
        random.shuffle(data_set)
        for line in data_set:
                line =line.split()
                line = line[4:6] + line[7:14] + [line[-1]]
                line = map(float, line)
                X.append(line[:-1])
                Y.append(line[-1])

if len(sys.argv) <= 2:
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.2, random_state=0)
else:
        X_train = X
        y_train = Y
        with open(sys.argv[2], 'r') as in_file:
                data_set = in_file.readlines()
                random.shuffle(data_set)
                for line in data_set:
                        line =line.split()
                        line = line[4:6] + line[7:14] + [line[-1]]
                        line = map(float, line)
                        X_test.append(line[:-1])
                        y_test.append(line[-1])

#scaler = preprocessing.StandardScaler().fit(X)
#X = scaler.transform(X)
#X_test = scaler.transform(X_test)
print np.sum(y_train), "pos samples out of", len(y_train)
print np.sum(y_test), "pos samples out of", len(y_test)


a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
clf1 = LogisticRegressionCV(Cs = a)
#clf1 = RandomForestClassifier(n_estimators = 100)

clf1.fit(X_train, y_train)
try:
        print "Feature importance:", clf1.feature_importances_
except AttributeError:
        print "Weight", clf1.coef_.tolist(), clf1.intercept_
print "Train score:",clf1.score(X_train, y_train)
print "Test score:", clf1.score(X_test, y_test)


#print search_for_best_features(np.array(X), np.array(X_test), np.array(X_val), Y, Y_test, Y_val, clf1)


