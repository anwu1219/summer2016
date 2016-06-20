#!/bin/bash

for i in {1..100}
do
y=10
for file in $i-*.dimacs
do
echo $file
j=$(((i-1)/y))
j=$((j+1))
mv $file f$j
done
done
