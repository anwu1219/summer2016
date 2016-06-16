#!/bin/bash
cd f4
for file in f4/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*