#!/bin/bash

for file in f10/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*