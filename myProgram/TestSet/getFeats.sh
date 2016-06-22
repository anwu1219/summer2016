rm feats.txt
rm featsTs.txt
parallel python graph.py {} ::: *.dimacs &
mv feats.txt featTs.txt
