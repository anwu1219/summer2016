#!/bin/bash

for file in testFeatures/*
do
    python regression.py $file
done



