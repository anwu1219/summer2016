import csv_reader

"""
This file replaces the previous model results by the rank model results. The
reason that I chose substitution instead of addition is that I don't need to 
change the other files this way and I already had the results from the regression
models. 
"""
csv_file = "csv/rankLst2.csv"
txt_file = "txt/totalRuntime2.txt"
def main():
    
    csvFile = csv_reader.read(csv_file)
    intxt = open()
    content = intxt.readlines()
    intxt.close()
    out = open("txt/totalRuntime2-rank.txt",'w')
    i = 0
    file_index = 0
    for line in content:
        if i % 302 == 0:
            file_index = int(line.split(".")[0].split("-")[-1])-1
        if i % 302 < 2:
            line = line.split(" ")
            line[1] = csvFile[file_index][1]
            line[2] = csvFile[file_index][2]
            line = " ".join(line)+"\n"
        out.write(line)
        i+=1
    out.close()

if __name__ == "__main__":
    main()
