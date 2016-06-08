"""
Reads in spreadsheet as numpy ndarray. 

Author: Andrew Becker
"""

import cPickle, numpy as np, scipy, sklearn, csv

def read(filename):
    """ Returns numpy ndarray containing values in csv
    """
    csvfile = open(filename,"rb")
    filereader = csv.reader(csvfile,delimiter=',',quotechar='"')
    
    m=0
    n=0
    for row in filereader:
        m+=1
        n=max(n,len(row))
    csvfile.seek(0)
    
    train_data = np.ndarray(shape=(m,n),dtype=object)

    i=0
    for row in filereader:
        for j in range(len(row)):
            np.put(train_data,i*n+j,row[j])
        i+=1
    
    return train_data
"""
data=read("1331.csv")
for j in range(data.shape[1]):
    for i in range(data.shape[0]):
        if ":" in data[i][j]:
            mins=(float)(data[i][j].split(":")[0])
            secs=(float)(data[i][j].split(":")[1])
            data[i][0]=mins*60.0+secs
        elif data[i][j]!="":
            data[i][j]=(float)(data[i][j])
"""