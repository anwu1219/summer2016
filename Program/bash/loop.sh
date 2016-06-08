#!/bin/bash

for file in allResults/newksat/*
do
    python graph.py $file
done

mv 1strandom_*.txt allResults/experiment/

