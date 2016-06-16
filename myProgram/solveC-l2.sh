#!/bin/bash

for file in f2/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*