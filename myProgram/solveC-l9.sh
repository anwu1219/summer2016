#!/bin/bash

for file in f9/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
