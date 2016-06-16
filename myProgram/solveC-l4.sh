#!/bin/bash
cd f1
for file in *.dimacs
do
echo $file
python miniSolv.py $file

done
cd ..
#rm temp*
