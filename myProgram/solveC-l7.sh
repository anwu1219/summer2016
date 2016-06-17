#!/bin/bash

for file in f7/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
