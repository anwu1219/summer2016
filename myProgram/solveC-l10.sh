#!/bin/bash

for file in f10/*.dimacs
do
echo $file
python miniSolv.py $file

done

#rm temp*
