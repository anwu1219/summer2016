import numpy as np
import sys
def main():
    """
    This file is used for the rank model. It computes the variable with the
    highest score.
    """
    read = open(sys.argv[1])
    content = read.readlines()
    read.close()
    i = 0
    
    for line in content:
        if i%300 == 0:
            if i != 0:
                print i/300,',', np.argmax(Y)+1
            Y = []
        Y.append(line.split()[-1])
        i += 1
    print i/300,',', np.argmax(Y)+1
if __name__ == "__main__":
    main()
    
