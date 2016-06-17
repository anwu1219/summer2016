#!/bin/bash

for file in f4/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
