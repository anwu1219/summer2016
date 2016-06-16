#!/bin/bash
cd f6
for file in f6/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*