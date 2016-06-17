#!/bin/bash

for file in f8/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
