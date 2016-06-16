#!/bin/bash

for file in f8/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*