from sklearn import preprocessing
import sys
sys.path.append("/Library/Python/2.7/site-packages")
import community
import networkx as nx
import numpy as np
#import csv
#import matplotlib.pyplot as plt

"""
This file takes in a dimacs file, calculates the features of it and stores them in a 
.txt file.
"""
def main():
    source = sys.argv[1]
    cnf = open(source)
    content = cnf.readlines()[1:]

    #Computing formula features
    parameters = content[0].split() 
    formula = content[1:] # The clause part of the dimacs file
    num_vars = int(parameters[2]) # AW Number of variables
    num_clause = int(parameters[3]) # AW Number of variables
    VIG = nx.Graph() 
    VIG.add_nodes_from(range(num_vars+1)[1:])
    VCG = nx.Graph()
    VCG.add_nodes_from(range(num_vars + num_clause + 1)[1:])
    preprocess_VIG(formula, VIG) # Build a VIG
    preprocess_VCG(formula, VCG, num_vars) # Build a VCG
    features = add_stat(VIG.degree().values())
    features += add_stat(VCG.degree().values()[:num_vars])
    part_VIG = community.best_partition(VIG)
    mod_VIG = community.modularity(part_VIG,VIG) # Modularity of VIG
    part_VCG = community.best_partition(VCG)
    mod_VCG = community.modularity(part_VCG,VCG) # Modularity of VCG
    features.append(mod_VIG)
    features.append(mod_VCG)
    # values = [part_VCG.get(node) for node in VCG.nodes()]
    # nx.draw_spring(VCG, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
    # plt.show()
    #features_all = preprocessing.scale(features_all)
    with open("feats.txt", 'a') as out_file:
        out_file.write(source.split(".")[0] + " " + " ".join(map(str, features)) + "\n")


    

def preprocess_VIG(formula, VIG):
    """
    Builds VIG.
    """
    for cn in range(len(formula)):
        formula[cn] = formula[cn].split()[:-1]
        for i in range(len(formula[cn])):
            formula[cn][i] = int(formula[cn][i])
        for i in range(len(formula[cn])-1):
            for j in range(len(formula[cn]))[i+1:]:
                VIG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]))    

def preprocess_VCG(formula, VCG, num_vars):
    """
    Builds VCG
    """
    for cn in range(len(formula)):
        for var in formula[cn]:
            VCG.add_edge(abs(var), cn + num_vars + 1)    

    
    
def construct_and_calculate(formula, num_vars, index, ratio_incls, ratio_var, 
                            deg_var_VCG, deg_var_VIG): 
    """
    A mistake is made here. This calculates the number of binary clauses, not 
    the number of horn clauses.
    """
    num_horn = 0
    count_vars_pos = [0] * num_vars
    count_vars_neg = [0] * num_vars    
    for cn in range(len(formula)):
        c = formula[cn]
        if (len(c) == 2):
            num_horn += 1
        pos_cnt = 0
        for i in range(len(c)):
            if c[i] < 0:
                count_vars_neg[abs(c[i])-1] += 1
            else:
                pos_cnt += 1
                count_vars_pos[c[i]-1] += 1
            deg_var_VCG[abs(c[i])-1] += 1
        ratio_incls.append(pos_cnt * 1.0/len(c))
        for i in range(len(c)-1):
            for j in range(len(c))[i+1:]:
                deg_var_VIG[abs(c[i])-1] += 1
                deg_var_VIG[abs(c[j])-1] += 1
    
    count_vars_pos.pop(index-1)
    count_vars_neg.pop(index-1)
    deg_var_VCG.pop(index-1)
    deg_var_VIG.pop(index-1)
    for i in range(len(count_vars_pos)):
        if count_vars_pos[i] + count_vars_neg[i] == 0:
            ratio_var.append(0)
        else:
            ratio_var.append(count_vars_pos[i]*1.0/(count_vars_pos[i] + count_vars_neg[i]))
    return num_horn

def add_stat(lst):
    """
    add max, min, mean, std of the give statistics to the features list.
    """
    return [max(lst),min(lst), np.mean(lst), np.std(lst)]
    
if __name__ == "__main__":
    main()