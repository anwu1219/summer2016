#!/bin/bash
cd f8
for file in f8/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*