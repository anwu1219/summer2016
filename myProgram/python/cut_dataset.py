import sys
import random


in_file_name = sys.argv[1]
ratio = float(sys.argv[2])
out_file_name = sys.argv[3]
out_file = open(out_file_name, 'w')
with open(in_file_name, 'r') as in_file:
    for line in in_file:
        if random.randint(1, 100) / 100.0 < ratio:
            out_file.write(line)
out_file.close()
        
