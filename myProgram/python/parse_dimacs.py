

import sys

content = []
with open(sys.argv[1], 'r') as input_file:
    for line in input_file:
        if len(line.split()) > 1:
            content.append(line)

with open(sys.argv[1], 'w') as output_file:
    for line in content:
        output_file.write(line)
