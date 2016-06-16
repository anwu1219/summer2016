#!/bin/bash
cd f1
for file in f1/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*