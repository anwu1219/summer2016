#!/bin/bash
cd f7
for file in f7/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*