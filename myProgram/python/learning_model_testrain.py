from sklearn import metrics
import numpy as np
from sklearn.linear_model import RidgeCV, LogisticRegressionCV, LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import preprocessing
import sys
from sklearn.preprocessing import PolynomialFeatures
from sklearn.externals import joblib
import random

def search_for_best_features(X, X_test, Y, Y_test, clf):
	new_X = X[:, 0:1]
	new_X_test = X_test[:, 0:1]
        lst = []
	clf.fit(new_X, Y)
	last_score = clf.score(new_X_test, Y_test)
	for i in range(len(X[0])):
                print i + 1, last_score
		new_X1 = np.append(new_X, X[:, i : i + 1], axis=1)
		new_X_test1 = np.append(new_X_test, X_test[:, i : i + 1], axis=1)
		current_score = clf.fit(new_X1, Y).score(new_X_test1, Y_test)
                #	if (current_score > last_score):
                lst.append(i + 1)
                new_X = new_X1
                new_X_test = new_X_test1
                last_score = current_score
        clf.fit(new_X, Y)
        print "Test:", clf.score(new_X_test, Y_test)
        print "Feature chosen:", lst


def single_feature_behavior(X, X_test, Y, Y_test, clf):
        for i in range(len(X[0])):
                new_X = np.array(X)[:, i : i + 1]
                new_X_test = np.array(X_test)[:, i : i + 1]
                clf.fit(new_X, Y)
#                print "Feature %d train score:" %(i + 1), clf.score(new_X, Y)
                print "Feature %d test score:" %(i + 1), clf.score(new_X_test, Y_test)



TRAIN_FILE_NAME = sys.argv[1] # used to build the models
TEST_FILE_NAME = sys.argv[2]
from random import shuffle

testscore = []

for z in range(20):
        interval = 10
        lower = 100 +  z * interval
        print lower, "-", lower + interval
        X = []
        Y = []
        X_test = []
        Y_test = []
    #    s = set()
        with open(TRAIN_FILE_NAME, 'r') as in_file:
                data_set = in_file.readlines()
                random.shuffle(data_set)
                for line in data_set:
                        line =line.split() # skip the formula identifier, num_var, and num_clause
                        #                if "uf100-" in line[0]:
                        if int(line[1]) >= lower and int(line[1]) <= lower + interval:

#                        if line[0].split("_")[0] not in s and int(line[1]) >= lower and int(line[1]) <= lower:
                                #if True:
                            #    s.add(line[0].split("_")[0])
                                #line = line[3:]
                                line = line[3:5] + line[6:16] + [line[-1]]
                                #line = line[4:6] + line[7:16] + [line[-1]]
                                line = map(float, line)
                                #                if line[-1] == 1 or random.randint(1,20) == 1:
                                
                                #               X.append([line[0]])
                                X.append(line[:-1])
                                Y.append(line[-1])
        with open(TEST_FILE_NAME, 'r') as in_file:
                data_set = in_file.readlines()
                random.shuffle(data_set)                                                                                                                                           
                for line in data_set:
                        line =line.split() # skip the formula identifier, num_var, and num_clause
                        if int(line[1]) >= lower and int(line[1]) <= lower + interval:
                        #if (line[0].split("_")[0]) not in s and int(line[1]) >= lower and int(line[1]) <= lower + 2:
                                #s.add(line[0].split("_")[0])
                                #line = line[3:]
                                line = line[3:5] + line[6:16] + [line[-1]]
                                line = map(float, line)
                                #                X_test.append([line[0]])
                                #                X_test.append(line[:-1])
                                X_test.append(line[:-1])
                                Y_test.append(line[-1])
        if len(X) > 10:
                #scaler = preprocessing.StandardScaler().fit(X)
                #X = scaler.transform(X)
                #X_test = scaler.transform(X_test)
                print np.sum(Y), "negative samples out of", len(Y), "in train set"
                print np.sum(Y_test), "negative samples out of", len(Y_test), "in test set.", "Baseline is", np.sum(Y_test)/len(Y_test)
                #poly = PolynomialFeatures(2)
                #X= poly.fit_transform(X)
                #X_test = poly.fit_transform(X_test)
                a = [1e-6, 1e-5, 1e-4, 0.001,0.01, 0.1, 1.0, 10.0,100]
                if sys.argv[3] == 'rf':
                        print "Random Forest"
                        clf1 = RandomForestClassifier(n_estimators = 100,  n_jobs = -1)
                elif sys.argv[3] == 'lr': 
                        print "Logistic Regression"
                        #clf1 = DecisionTreeClassifier()
                        #clf1 = KNeighborsClassifier(n_neighbors = 11, n_jobs = -1, weights = 'distance')
                        clf1 = LogisticRegressionCV(Cs=a)
                elif sys.argv[3] == 'svc':
                        print "Linear SVC"
                        clf1 = LinearSVC()
                        
                        #clf1 = AdaBoostClassifier(n_estimators = 1000)
                        # print "Learning..."
                        
                        
                #clf1 = joblib.load("testcasesForMLSat/prob_feat4/prob_feat4.pkl")
                clf1.fit(X, Y)
                if len(sys.argv) > 4 and sys.argv[4] == 'coefs':
                        try:
                                print "Feature importance:", clf1.feature_importances_ 
                        except AttributeError:
                                print "Weight", clf1.coef_.tolist(), clf1.intercept_
                print "Train score:",clf1.score(X, Y)
                testscore.append(clf1.score(X_test, Y_test))
                print "Test score:", testscore[-1]
for ele in testscore:
        print ele
#joblib.dump(clf1, 'testcasesForMLSat/prob_feat4/prob_feat4.pkl')


#confidence = []
#nums_conf = []
#high_prob_score = []

#for j in range(21):
#        try:
#                probs =  clf1.predict_proba(X_test)[:,1]
#                X_test_hp = []
#                Y_test_hp = []
#                confidence.append(0.9 + j * 0.005)
#                for i in range(len(probs)):
#                        if probs[i] > 0.9 + j * 0.005 or probs[i] < 0.1 - j * 0.005:
#                                X_test_hp.append(X_test[i])
#                                Y_test_hp.append(Y_test[i])
#        except:
#                probs = clf1.decision_function(X_test)
#                X_test_hp = []
#                Y_test_hp = []
#                confidence.append(1.5 + j * 0.05)
#                for i in range(len(probs)):
#                        if probs[i] > 1.5 + j * 0.05 or probs[i] < -1.5 - j * 0.05:
#                                X_test_hp.append(X_test[i])
#                                Y_test_hp.append(Y_test[i])
#        nums_conf.append(len(X_test_hp))
#        if (len(X_test_hp) == 0):
#                break
#        high_prob_score.append(clf1.score(X_test_hp, Y_test_hp))
# #predict2 = clf2.score(X_test, Y_test)
# 	print predict1
# except ValueError:
# 	print "fail"
#print confidence
#print nums_conf
#print high_prob_score

if len(sys.argv) > 3 and sys.argv[3] == '-s':
        single_feature_behavior(X, X_test, Y, Y_test, clf1)


#search_for_best_features(np.array(X), np.array(X_test), Y, Y_test, clf1)


