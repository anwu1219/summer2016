#!/bin/bash

for file in f1/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
