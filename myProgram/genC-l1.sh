#!/bin/bash

for file in f1/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*