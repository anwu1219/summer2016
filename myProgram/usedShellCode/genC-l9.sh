#!/bin/bash

for file in f9/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*