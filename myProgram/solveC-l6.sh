#!/bin/bash

for file in f6/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*