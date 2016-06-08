#!/bin/bash

for file in newksat-*
do
    python data_collect.py $file
done
