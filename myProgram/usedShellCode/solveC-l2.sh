#!/bin/bash

for file in f2/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
