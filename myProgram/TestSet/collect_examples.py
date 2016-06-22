import sys
import os


"""
This file takes in a updated formula name (e.g. 9-9), and updates a txt file that contains target variables, file name of original formulae, and deleted variable, and file name of updated formula
"""


def main():
	collect_file = sys.argv[1]
	formula = sys.argv[2].split('.')[0]
	updateCollect(collect_file, formula)


def updateCollect(collect_file, formula):
	if os.path.isfile(formula + "Sol.txt"):
		with open(formula + "Sol.txt", 'r') as in_file:
                        try:
                                if "UNSAT" in in_file.readlines()[0]:
                                        tar = 0
                                        with open(collect_file,'a') as out_file:
                                                out_file.write(formula + " " + str(tar) + "\n")
                                              #  out_file.write(formula + " " + formula.split("-")[0] + " " + formula[(len(formula.split("-")[0]) + 1):] + " " + str(tar) + "\n")
                                else:
                                        tar = 1
                                        with open(collect_file,'a') as out_file:
                                                out_file.write(formula + " " + str(tar) + "\n")
#                                                out_file.write(formula + " " + formula.split("-")[0] + " " + formula[(len(formula.split("-")[0]) + 1):] + " " + str(tar) + "\n")
                        except IndexError:
                                print formula, "is empty"


if __name__ == "__main__":
    main()
