#!/bin/bash

for file in *.dimacs
do
    echo $file
    python miniSolv.py $file
# What does ">" do
#java -jar RankLib-2.1-patched.jar -silent -load myModel-6.txt -rank temp_features.txt -score temp_scores.txt
#python getFirst.py temp_scores.txt
done

#rm temp*
