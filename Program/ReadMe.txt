allResults contain the original 101 formulas (the number goes to 103 but I think 2 are missing). These formulas are used to obtain the training set. 

bash contains .sh files that call python functions or other functions in order.

csv contains .csv files that are used to construct models and compare results.

findRank.java takes in files like "totalRuntime.txt" in the txt folder and outputs the statistics for RandomForest and Ridge.

python contains python files. Each of them are documented.

RankLib-2.1-patched.jar builds ranking models. The detailed documentation can be found on https://sourceforge.net/p/lemur/wiki/RankLib/.

There are two testSets, the first containing 50 formulas and the second containing 100 formulas.

testFeatures contains the features obtained from the first testSet.
testFeatures2 contains the features obtained from the testSet2.

txt contains a bunch of txt files generated during experiment. Some of them do not make sense, but I thought it might be a good idea to keep them.
