#!/bin/bash

for file in f5/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
