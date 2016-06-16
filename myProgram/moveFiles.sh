#!/bin/bash

for i in {1..100}
do
y=10
for file in $i-*.dimacs
do
j=$(((i-1)/y))
j=$((j+1))
mv $i-*.dimacs f$j
done
done
