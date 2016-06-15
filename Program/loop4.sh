#!/bin/bash
i = 1
for file in allResults/newksat/*
do
    python python/calcRuntime.py $file > newksat-$i.txt
    i=$((i+1))
    mv $file done/
done