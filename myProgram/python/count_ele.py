import sys

with open(sys.argv[1], 'r') as in_file:
    print len(in_file.readlines()[1].split())
