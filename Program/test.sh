#!/bin/bash

for file in testFeatures/*
do
echo $file
python test.py $file > temp_features.txt
# What does ">" do
#java -jar RankLib-2.1-patched.jar -silent -load myModel-6.txt -rank temp_features.txt -score temp_scores.txt
#python getFirst.py temp_scores.txt
done

#rm temp*