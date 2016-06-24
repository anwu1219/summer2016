from sklearn import preprocessing
import sys
sys.path.append("/Library/Python/2.7/site-packages")
import community
import networkx as nx
import numpy as np
import scipy as sp
import math
import os
#import csv
#import matplotlib.pyplot as plt



"""
This file takes in a dimacs file, calculates the features of it and stores them in a 
.txt file.
"""
def main():
    source = sys.argv[1]
    cnf = open(source)
    content = cnf.readlines()
    while content[0].split()[0] == 'c':
        content = content[1:]

    while len(content[-1].split()) <= 1:
        content = content[:-1]

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
    features = []
    features.append(num_vars) 
    # print "1 num_vars", num_vars
    features.append(num_clause)
    # print "2 num_clause", num_clause
    # print "3 Clause variable ratio",float(num_clause) / num_vars
    features.append(float(num_clause) / num_vars) # Clause variable ratio
    # print "14-17 VIG degree features",add_stat(VIG.degree().values())[:-1]
    features += add_stat(VIG.degree().values())[:-1] # VIG degree features
    # print "4-8 VCG var degree features", add_stat(VCG.degree().values()[:num_vars])
    features += add_stat(VCG.degree().values()[:num_vars])  # VCG var degree features
    # print "9-13 VCG clause degree features", add_stat(VCG.degree().values()[num_vars:])
    features += add_stat(VCG.degree().values()[num_vars:])  # VCG clause degree features
    # print "18-20 Occurence of positive and negative literals in each clause", add_stat(get_pos_neg_ratio(formula))[2:]
    features += add_stat(get_pos_neg_ratio(formula))[2:]    # Occurence of positive and negative literals in each clause
    # print "21-25 Occurence of positive and negative literals for each variable", add_stat(get_pos_neg_occ(formula, num_vars))
    features += get_pos_neg_occ(formula, num_vars)   # Occurence of positive and negative literals for each variable
    # print "26-27 Ratio of binary clause", get_binary(formula, num_clause)
    features += get_binary(formula, num_clause)   # Ratio of binary clause
    # print "28/-28 29-33/ -29-33 Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features", horn_features(formula, num_vars, num_clause)
    features += horn_features(formula, num_vars, num_clause)[: -5] # Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features
    # print "Modularities of VIG & VCG", get_modularities(VIG, VCG, graphic = False)
    features += get_modularities(VIG, VCG, graphic = False) # Modularities of VIG & VCG
    features.append(get_LPSLACK_coeff_variation(formula, num_vars, num_clause))
    features += [isSat(sys.argv[1])]
    if features[-1] == -1:
        return
    if len(features) != 39:
        print len(features)
        print "shoot! The feature number doesn't match!"
    with open(sys.argv[2], 'a') as out_file:
        out_file.write(source.split(".")[0] + " " + " ".join(map(str, features)) + "\n")

#--------------------------------------------Target extraction methods--------------------------------------# 

def isSat(filename):
    """
    Opens the solution file and check the satisfiability of the formula
    """
    if os.path.isfile(filename.split()[0] + "Sol.txt"):
        with open(filename.split()[0]+"Sol.txt", 'r') as tar_file:
            try:
                if "UNSAT" in tar_file.readlines()[0]:
                    return 1
                else:
                    return 0
            except IndexError:
                print filename, "is empty"
                return -1

#--------------------------------------------feature extraction methods-------------------------------------#
def preprocess_VIG(formula, VIG):
    """
    Transforms a formula into int matrix
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

    
def get_pos_neg_ratio(formula):
    """ 
    get the ratio of positive occurrences of each literal at each line
    """
    lst = []
    for line in formula:
        pos = 0
        for ele in line:
            if ele > 0:
                pos += 1
        lst.append(float(pos) / len(line))
    return lst




def get_pos_neg_occ(formula, num_vars):
    """ 
    get the ratio of positive and negative occurrences of each variable
    """
    dic = {}
    lst = []
    for i in range(num_vars + 1)[1:]:
        dic[i] = [0, 0]
    for line in formula:
        for ele in line:
            dic[abs(ele)][0] = dic[abs(ele)][0] + 1
            if ele > 0:
                dic[abs(ele)][1] = dic[abs(ele)][1] + 1
    for i in range(num_vars + 1)[1:]:
        lst.append(float(dic[i][1]) / dic[i][0])
    POSNEG_ratio_var_mean = 0
    for i in range(num_vars + 1)[1:]:
        POSNEG_ratio_var_mean += abs((0.5 - dic[i][1]) / dic[i][0])

    return add_stat(lst) + [POSNEG_ratio_var_mean * 2 / num_vars]



def get_binary(formula, num_clause):
    """
    get the ratio of binary clauses, and ternary clauses
    """
    num_bi = 0
    num_ter = 0
    for line in formula:
        if len(line) == 2:
            num_bi += 1
        if len(line) == 3:
            num_ter += 1
    return [float(num_bi) / num_clause, float(num_ter) / num_clause]


#--------------------------------------------horn-related features-----------------------------------------#


def horn_features(formula, num_vars, num_clause):
    """
    Formats the outputs of ratio_horn_clauses(), returns processed 10 features related to horn clauses
    """
    ratio_horn, ratio_rev_horn, lst = ratio_horn_clauses(formula, num_vars, num_clause)
    horn_var_feats = add_stat(lst[0])
    rev_horn_var_feats = add_stat(lst[1])
    return [ratio_horn, ratio_rev_horn] + horn_var_feats + rev_horn_var_feats

def ratio_horn_clauses(formula, num_vars, num_clause):
    """
    Get the ratiotion of horn clauses, reverse horn clauses in the formula, 
    as well as the occurence of each variable in horn clauses and reverse horn clauses
    """
    num_horn = 0
    num_rev_horn = 0
    dic = {}
    lst = [[],[]]   
    # the first row is the occrence of each variable in horn clauses, the second in reverse horn clauses
    for i in range(num_vars + 1)[1:]:
        dic[i] = [0, 0]
    for line in formula:
        num_pos, num_neg = pos_neg_lits(line)
        if num_pos <= 1:
            num_horn += 1
            for ele in line:
                dic[abs(ele)][0] += 1
        if num_neg <= 1:
            num_rev_horn += 1
            for ele in line:
                dic[abs(ele)][1] += 1
    for i in range(num_vars + 1)[1:]:
        lst[0].append(dic[i][0])
        lst[1].append(dic[i][1])
    return 1.0 * num_horn / num_clause, 1.0 * num_rev_horn / num_clause, lst

def pos_neg_lits(clause):
    # This is a helper function for ratio_horn_clauses(); 
    # returns the number of positive literals in a clause
    # in the case of 3^(-)-cnf, which is our case, if a clause is not a horn clause, 
    # then it is a reverse horn clause 
    new_clause = np.array(clause)
    return (new_clause > 0).sum(), (new_clause < 0).sum()


#------------------------------------------modularity-related features-------------------------------------#


def get_modularities(VIG, VCG, graphic):
    """
    Returns the modularities of VIG and VCG representations of the formula
    """
    part_VIG = community.best_partition(VIG)
    mod_VIG = community.modularity(part_VIG,VIG) # Modularity of VIG
    part_VCG = community.best_partition(VCG)
    mod_VCG = community.modularity(part_VCG,VCG) # Modularity of VCG
    if graphic:
        values = [part_VCG.get(node) for node in VCG.nodes()]
        nx.draw_spring(VCG, cmap=plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
        plt.show()
        features_all = preprocessing.scale(features_all)
    return [mod_VIG, mod_VCG]


#-------------------------------------------LPSLACK coeff variation----------------------------------------#

def get_LPSLACK_coeff_variation(formula, num_vars, num_clause):
    v = [0.0] * num_vars
    for line in formula:
        for ele in line:
            if ele > 0:
                v[ele - 1] -= 1
            else:
                v[abs(ele) - 1] += 1
    #print v, num_clause
    A_ub = []
    for i in range(num_clause):
        A_ub.append([0.0] * num_vars)
    b = [-1.0] * num_clause
    for i in range(num_clause):
        for ele in formula[i]:
            if ele > 0:
                A_ub[i][ele - 1] -= 1
            if ele < 0:
                A_ub[i][abs(ele) - 1] += 1
                b[i] += 1
    bounds = (0.0, 1.0)
    v_star = sp.optimize.linprog(c = v, A_ub = A_ub, b_ub= b, bounds = bounds)
    #print v_star
    v_star = v_star.x


    try:
        if math.isnan(v_star):
            return 0
    except TypeError:
        for i in range(len(v_star)):
            v_star[i] = min(v_star[i], 1 - v_star[i])
    if np.mean(v_star) == 0:
        return 0
    result = np.std(v_star) / np.mean(v_star)
    return result

#-----------------------------------------------statistics-------------------------------------------------#

def add_stat(lst):
    """
    add max, min, mean, std of the give statistics to the features list.
    """
    return [max(lst),min(lst), np.mean(lst), np.std(lst), sp.stats.entropy(lst)]
    
if __name__ == "__main__":
    main()
