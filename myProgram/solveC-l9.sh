#!/bin/bash
cd f9
for file in f9/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*