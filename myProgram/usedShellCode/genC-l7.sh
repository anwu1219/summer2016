#!/bin/bash

for file in f7/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*