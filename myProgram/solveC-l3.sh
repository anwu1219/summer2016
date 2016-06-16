#!/bin/bash
cd f3
for file in f3/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*