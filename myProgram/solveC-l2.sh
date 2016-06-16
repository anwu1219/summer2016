#!/bin/bash
cd f2
for file in f2/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*