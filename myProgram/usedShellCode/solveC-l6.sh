#!/bin/bash

for file in f6/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
