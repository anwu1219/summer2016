#!/bin/bash

for file in f3/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
