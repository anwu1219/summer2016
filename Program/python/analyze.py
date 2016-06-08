import csv_reader,csv_writer,random
import numpy as np
from sklearn import neural_network
from sklearn import preprocessing
from sklearn.svm import SVC, LinearSVC, SVR, LinearSVR
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostRegressor,GradientBoostingRegressor, BaggingRegressor, ExtraTreesRegressor
from sklearn.linear_model import LogisticRegressionCV, RidgeCV
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cross_validation import KFold
"""
This file is used for applying machine learning to an already processed dataset.
The dataset has to be in csv format, where the last column is the target variable.
"""

FILENAME = "featuresAll.csv"
def numerical(data):
    """
    Transform string into float.
    """    
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return

"""
Read in data and cut into a training set and a test set.
"""
data=csv_reader.read(FILENAME)
np.random.shuffle(data)
m,n=data.shape
numerical(data)
data = data.transpose()
features = data[:-1]
targets = data[-1]
features = features.transpose()
targets = targets.transpose()
cut = 0.8 * m

train_features = features[:cut]
train_targets = targets[:cut]
test_features = features[cut:]
test_targets= targets[cut:]


def main():
    """
    Choose models to present here.
    """
    #present(DummyClassifier(strategy = 'most_frequent'))
    #present(SVC(kernel = "rbf"))
    #present(RidgeCV(alphas = [0.0001,0.001,0.01,0.1,1,10,100]))
    #present(RandomForestRegressor(n_estimators = 30))
    #present(AdaBoostRegressor())
    #present(GradientBoostingRegressor())
    #present(ExtraTreesRegressor())
    #present(BaggingRegressor())
    #present(SVR(kernel = 'poly'))
    #present(RandomForestClassifier(n_estimators = 300, criterion = 'entropy'))
    #present(LogisticRegressionCV(Cs=[0.0001,0.001,0.01,0.1,1,10,100,100]))
    #present(KNeighborsClassifier(n_neighbors = 2))
    #knn()
    return

def present(model):
    """
    Present the score and mse of this model. For classification, score is accuracy 
    and for regression, score is R^2. You can also choose to build a confusion 
    matrix if the model is a classification model.
    """
    model.fit(train_features, train_targets)
    pred = model.predict(test_features)
    print model.score(test_features,test_targets), mse(pred, test_targets)
    #print build_confusion(pred, test_targets)

def mse(pred, act):
    """
    Calculating the mean squared error.
    """
    e = 0
    for i in range(len(pred)):
        e += (pred[i] - float(act[i]))**2
    return e

def knn():
    """
    This method used cross-validation to tune the number of neighbors in KNN. 
    After determining n, please present the KNN model with the specified n.
    """
    kf = KFold(len(train_features), 5)
    N_RANGE = range(15)[1:]
    highest_score = 0
    for n in N_RANGE:
        total_score = 0
        for train_index, test_index in kf:
            X_train, X_test = train_features[train_index], train_features[test_index]
            y_train, y_test = train_targets[train_index], train_targets[test_index]
            neigh = KNeighborsClassifier(n_neighbors = n, n_jobs = -1)
            neigh.fit(X_train, y_train)
            total_score += neigh.score(X_test, y_test)
        if total_score > highest_score:
            n_final = n
            highest_score = total_score
    print n_final
    
def build_confusion(pred, act):
    """
    Builds a confusion model, which looks like this:
    =======
    TP | FN
    -------
    FP | TN
    =======
    """
    mat = np.zeros([2,2])
    for i in range(len(pred)):
        if float(pred[i]) == 1.0 and float(act[i]) == 1.0:
            mat[0,0] += 1
        elif float(pred[i]) == 0.0 and float(act[i]) == 1.0:
            mat[1,0] += 1
        elif float(pred[i]) == 1.0 and float(act[i]) == 0.0:
            mat[0,1] += 1
        else:
            mat[1,1] += 1
    return mat



if __name__ == "__main__":
    main()


