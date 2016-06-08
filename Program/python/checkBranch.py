import subprocess
import timeAfterReg
def main():
    in_file = open("branchingV2.txt",'r')
    contentBV = in_file.readlines()
    in_file.close()
    for line in contentBV:
        line = line.split()
        cnf_name = "testSet2/" + line[0].split("/")[1].split(".")[0] + ".dimacs"
        print cnf_name, line[1]
        #subprocess.call(["python timeAfterReg.py",cnf_name,line[1]])
        timeAfterReg.process(cnf_name, line[1])
if __name__ == "__main__":
    main()
