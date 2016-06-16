#!/bin/bash
y=10
for i in {1..100}
do
for file in $i-*.dimacs
do
j=$(((i-1)/y))
j=$((j+1))
echo $j
#mv $i-*.dimacs f$j
done
done