#!/bin/bash

for file in f5/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*