#!/bin/bash
cd f5
for file in f5/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*