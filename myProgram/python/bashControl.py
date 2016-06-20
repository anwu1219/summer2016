
import sys
import os

# This file controls parallel shell code files.
def main():
	if sys.argv[1] == '-c': # copy file argv[2] to file argv[3]
		with open(sys.argv[2], 'r') as in_file: # Read a dimacs file
			in_content = in_file.readlines()
		with open(sys.argv[3], 'w') as out_file:
			for line in in_content:
				out_file.write(line)
	if sys.argv[1] == '-r': # replace the argv[3]th line of argv[2] with argv[4] 
		changedIndex = int(sys.argv[3]) - 1
		with open(sys.argv[2], 'r') as in_file: # Read a dimacs file
			in_content = in_file.readlines()
		os.remove(sys.argv[2])
		with open(sys.argv[2], 'w') as out_file:
			for i in range(len(in_content)):
				if i != changedIndex:
					out_file.write(in_content[i])
				else:
					out_file.write(sys.argv[4] + "\n")



if __name__ == "__main__":
    main()
