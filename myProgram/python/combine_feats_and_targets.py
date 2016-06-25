import sys
import operator


feats_file_name = sys.argv[1] # used to build the models
targets_file_name = sys.argv[2]
out_file_name = sys.argv[3]



with open(feats_file_name, 'r') as in_file:
	features = in_file.readlines()
	for i in range(len(features)):
		features[i] = features[i].split()
features.sort(key=operator.itemgetter(0))

with open(targets_file_name, 'r') as in_file:
	targets = in_file.readlines()
	for i in range(len(targets)):
		targets[i] = targets[i].split()
targets.sort(key=operator.itemgetter(0))

with open(out_file_name, 'w') as out_file:
        j = 0
	for i in range(len(features)):
		if features[i][0] == targets[j][0]:
			line = " ".join(features[i]) + " " + targets[j][-1]
			out_file.write(line + "\n")
		else:
			print "not matched"
			print features[i][0], targets[j][0]
			j += 1
                j += 1
