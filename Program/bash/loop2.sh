#!/bin/bash

for file in testSet2/*
do
    python graph.py $file
done

mv test2_ksat-*.txt testFeatures2/

