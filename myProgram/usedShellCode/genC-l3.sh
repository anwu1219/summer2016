#!/bin/bash

for file in f3/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*