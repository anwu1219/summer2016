from sklearn import preprocessing
import sys
sys.path.append("/Library/Python/2.7/site-packages")

import networkx as nx
import numpy as np
import copy
import timeit
"""
This file takes in a dimacs file, calculates the features of it and stores them in a 
.txt file.
"""
def main():
    source = sys.argv[1]
    cnf = open(source)
    content = cnf.readlines()[1:]
    cnf_name = source.split("/")[-1].split(".")[0] + "feats.txt"

    #Computing formula features
    parameters = content[0].split() 
    formula = content[1:] # The clause part of the dimacs file
    num_vars = int(parameters[2]) # AW Number of variables
    VG = nx.Graph()
    VG.add_nodes_from(range(num_vars+1)[1:])
    preprocess(formula, VG, num_vars)
    features_all = []
    write_to_features(new_formula_pos, new_formula_neg, features_all, i, num_vars)
    features_all = preprocessing.scale(features_all)
    
    with open(cnf_name, 'w') as doc: # AW Write each variable as an instance 
        for i in range(num_vars):
            doc.write(str(i+1)+":")
            for j in range(feature.shape[1]):
                doc.write(str(feature[i,j]) + ",")
            for j in range(len(features_all[i])):
                doc.write(str(features_all[i][j]) + ",")
            doc.write("\n")
    doc.close()

def preprocess(formula, VG, num_vars):
    """
    Builds VIG.
    """
    for cn in range(len(formula)):
        formula[cn] = formula[cn].split()[:-1]
        for i in range(len(formula[cn])):
            formula[cn][i] = int(formula[cn][i])
        for i in range(len(formula[cn])-1):
            for j in range(len(formula[cn]))[i+1:]:
                VG.add_edge(abs(formula[cn][i]), abs(formula[cn][j]))    

def trim_formula(formula, var): 
    """
    Update formula after setting a variable.
    """
    new = copy.deepcopy(formula)
    cn = 0
    while cn < len(new):
        c = new[cn]
        if var in c:
            new.pop(cn)
        else:
            try:
                c.remove(-var)
            except:
                pass
            cn += 1
    return new
    
    
def write_to_features(f_pos, f_neg, features_all, i, num_vars):
    """
    writes all the formula features into a matrix called "features" and then 
    add that to "features_all".
    """
    ratio_incls_pos = []
    ratio_incls_neg = []
    ratio_var_pos = []
    ratio_var_neg = []
    deg_var_VCG_pos = [0] * num_vars
    deg_var_VCG_neg = [0] * num_vars
    deg_var_VG_pos = [0] * num_vars
    deg_var_VG_neg = [0] * num_vars
    num_horn_pos = construct_and_calculate(f_pos, num_vars, i, ratio_incls_pos, 
                                           ratio_var_pos, deg_var_VCG_pos, 
                                           deg_var_VG_pos)
    num_horn_neg = construct_and_calculate(f_neg, num_vars, i, ratio_incls_neg, 
                                           ratio_var_neg, deg_var_VCG_neg, 
                                           deg_var_VG_neg)
    features = []
    add_stat(deg_var_VG_pos, features)
    add_stat(deg_var_VG_neg, features)
    add_stat(deg_var_VCG_pos, features)
    add_stat(deg_var_VCG_neg, features)
    add_stat(ratio_var_pos, features)
    add_stat(ratio_var_neg, features)
    add_stat(ratio_incls_pos, features)
    add_stat(ratio_incls_neg, features)
    features.append(num_horn_pos)
    features.append(num_horn_neg)
    features_all.append(features)
    
def construct_and_calculate(formula, num_vars, index, ratio_incls, ratio_var, 
                            deg_var_VCG, deg_var_VG): 
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
                deg_var_VG[abs(c[i])-1] += 1
                deg_var_VG[abs(c[j])-1] += 1
    
    count_vars_pos.pop(index-1)
    count_vars_neg.pop(index-1)
    deg_var_VCG.pop(index-1)
    deg_var_VG.pop(index-1)
    for i in range(len(count_vars_pos)):
        if count_vars_pos[i] + count_vars_neg[i] == 0:
            ratio_var.append(0)
        else:
            ratio_var.append(count_vars_pos[i]*1.0/(count_vars_pos[i] + count_vars_neg[i]))
    return num_horn

def add_stat(lst, features):
    """
    add max, min, mean, std of the give statistics to the features list.
    """
    features.append(max(lst))
    features.append(min(lst))
    features.append(np.mean(lst))
    features.append(np.std(lst))
    
if __name__ == "__main__":
    main()