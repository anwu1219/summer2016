#!/bin/bash

for file in first10ofharderSat/*.dimacs
do
echo $file
python getBB.py $file

done

#rm temp*