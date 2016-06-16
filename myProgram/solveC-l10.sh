#!/bin/bash
cd f10
for file in f10/*.dimacs
do
echo $file
python getBB.py $file

done
cd ..
#rm temp*