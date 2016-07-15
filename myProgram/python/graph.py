from sklearn import preprocessing
import sys
import subprocess
sys.path.append("/Library/Python/2.7/site-packages")
import community
import networkx as nx
import numpy as np
import scipy as sp
import math
from pulp import *
from sets import Set
import timeit
#import csv
#import matplotlib.pyplot as plt



"""
This file takes in a dimacs file, calculates the features of it and stores them in a 
.txt file.
"""
def main():
#    source = argv1
#    except:
    source = sys.argv[1]
#    try: 
#    SAT = argv2
#    except:
    SAT = sys.argv[2]
#    try:
#    out_name = argv3
#    except:
    out_name = sys.argv[3]
    cnf = open(source)
    content = cnf.readlines()
    while content[0].split()[0] == 'c':
        content = content[1:]
    while len(content[-1].split()) <= 1:
        content = content[:-1]
    content = remove_duplicate(content)
    #Computing formula features
    parameters = content[0]
    formula = content[1:] # The clause part of the dimacs file
    num_vars = int(parameters[2]) # AW Number of variables
    if num_vars == 0:
        return
    num_clause = int(parameters[3]) # AW Number of variables
    if num_clause == 0:
        return 
    start = timeit.default_timer()
    VIG = nx.Graph() 
    VIG.add_nodes_from(range(num_vars+1)[1:])
    VCG = nx.Graph()
    VCG.add_nodes_from(range(num_vars + num_clause + 1)[1:])
    preprocess_VIG(formula, VIG) # Build a VIG
    preprocess_VCG(formula, VCG, num_vars) # Build a VCG
    features = []
    features.append(num_vars) 
    # print "1 num_vars", num_vars
#    features.append(num_clause)
    # print "2 num_clause", num_clause
    # print "3 Clause variable ratio",float(num_clause) / num_vars
    features.append(float(num_clause) / num_vars) # Clause variable ratio
    # print "14-17 VIG degree features",add_stat(VIG.degree().values())[:-1]
#    features += add_stat_normalized(VIG.degree().values(), num_vars) # VIG degree features
    # print "4-8 VCG var degree features", add_stat(VCG.degree().values()[:num_vars])
#    features += add_stat_normalized(VCG.degree().values()[:num_vars], num_vars)  # VCG var degree features
    # print "9-13 VCG clause degree features", add_stat(VCG.degree().values()[num_vars:])
#    features += add_stat_normalized(VCG.degree().values()[num_vars:], num_vars)  # VCG clause degree features
    # print "18-20 Occurence of positive and negative literals in each clause", add_stat(get_pos_neg_ratio(formula))[2:]
    features += add_stat(get_pos_neg_ratio(formula))[2:]    # Occurence of positive and negative literals in each clause
    # print "26-27 Ratio of binary clause", get_binary(formula, num_clause)
    features += get_binary(formula, num_clause)   # Ratio of binary clause
    # print "28/-28 29-33/ -29-33 Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features", horn_features(formula, num_vars, num_clause)
    features += ratio_horn_clauses(formula, num_vars, num_clause) # Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features
    # print "Modularities of VIG & VCG", get_modularities(VIG, VCG, graphic = False)
    # print "21-25 Occurence of positive and negative literals for each variable", add_stat(get_pos_neg_occ(formula, num_vars))  
    features += get_pos_neg_occ(formula, num_vars)   # Occurence of positive and negative literals for each variable 
#    end = timeit.default_timer()
#    print "cheap features", end-start
#    start = timeit.default_timer()
#    features += get_modularities(VIG, VCG, graphic = False) # Modularities of VIG & VCG
#    end = timeit.default_timer()
#    print "mod",  end-start
#    start = timeit.default_timer()
     features += get_LPSLACK_coeff_variation(formula, num_vars, num_clause)
#    end =  timeit.default_timer()
#    print "LPSlack", end-start
#    start = timeit.default_timer()
    features += get_sat_prob(formula, num_vars)
#    end = timeit.default_timer()
#    print "sat_prob", end-start
    features += [SAT]
    with open(out_name, 'a') as out_file:
        out_file.write(source.split(".")[0] + " " + " ".join(map(str, features)) + "\n")


#--------------------------------------------feature extraction methods-------------------------------------#
def get_cl_string(clause):
    s = ""
    clause.sort()
    for ele in clause:
        s += str(ele) + "-"
    return s[:-1]

def remove_duplicate(content):
    new_content = [content[0].split()]
    cs = Set()
    num_clause = 0
    for line in content[1:]:
        line = map(int, line.split())[:-1]
        c = get_cl_string(line)
        if c not in cs:
            num_clause += 1
            new_content.append(line)
            cs.add(c)
    new_content[0][3] = num_clause
    return new_content

def preprocess_VIG(formula, VIG):
    """
    Transforms a formula into int matrix
    Builds VIG.
    """
    for cn in range(len(formula)):
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
        if len(line) != 0:
            pos = 0
            for ele in line:
                if ele > 0:
                    pos += 1
            lst.append(float(pos) / len(line))
        else:
            print "Line is empty", sys[1]
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
        if dic[i][0] != 0:
            lst.append(float(dic[i][1]) / dic[i][0])
    POSNEG_ratio_var_mean = 0
    for i in range(num_vars + 1)[1:]:
        if dic[i][0] != 0:
            POSNEG_ratio_var_mean += abs((0.5 - float(dic[i][1]) / dic[i][0])
        else:
            print "Can't find variable", i, sys.argv[1]
            num_vars -= 1
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
    horn_var_feats = add_stat_normalized(lst[0], num_vars)
   # rev_horn_var_feats = add_stat(lst[1])
    return [ratio_horn] + horn_var_feats# + rev_horn_var_feats

def ratio_horn_clauses(formula, num_vars, num_clause):
    """
    Get the ratiotion of horn clauses, reverse horn clauses in the formula, as well as the occurence of each variable in horn clauses and reverse horn clauses                
    """
    num_horn = 0
    num_rev_horn = 0
    for line in formula:
        num_pos, num_neg = pos_neg_lits(line)
        if num_pos <= 1:
            num_horn += 1
        if num_neg <= 1:
            num_rev_horn += 1
    return [1.0 * num_horn / num_clause, 1.0 * num_rev_horn / num_clause]#, lst                                                               



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

def get_LPSLACK_with_LP_Solve(formula, num_vars, num_clause):
    v = [0.0] * (num_vars + 1)
    for line in formula:
        for ele in line:
            if ele > 0:
                v[ele] += 1
            else:
                v[abs(ele)] -= 1
    s = ""
    for i in range(1, num_vars + 1):
        if v[i] > 0:
            if s == "":
                s = str(v[i]) + " x%d" %i
            else:
                s = s + " + %d x%d" %(v[i], i)
        elif v[i] < 0:
            if s == "":
                s = str(v[i]) + " x%d" %i
            else:
                s = s + " - %d x%d " %(abs(v[i]), i)
    s = "max: " + s[:-1] + ";\n";
    for i in range(num_clause):
        for j in range(len(formula[i])):
            if formula[i][j] < 0:
                s = s + "1 - x" + str(abs(formula[i][j])) + " + "
            else:
                s = s + "x" + str(abs(formula[i][j])) + " + "
        s = s[:-2] + ">= 1;\n"
    for i in range(1, num_vars + 1):
        s = s + "0 <= x%d  <= 1;\n" %i
    with open("s.lp", 'w') as out_file:
        out_file.write(s);
    subprocess.call("lp_solve s.lp", shell=True)


def get_LPSLACK_coeff_variation(formula, num_vars, num_clause):
    v = [0.0] * (num_vars + 1)
    for line in formula:
        for ele in line:
            if ele > 0:
                v[ele] += 1
            else:
                v[abs(ele)] -= 1

    LPVar = [0]
    for i in range(1, num_vars + 1):
        LPVar.append(LpVariable("x%d" %i, 0, 1))
    

    prob = LpProblem("problem", LpMaximize)
     

    for i in range(num_clause):
        exp = 0
        for j in range(len(formula[i])):
            if formula[i][j] < 0:
                exp = exp + 1 - LPVar[abs(formula[i][j])]
            else:
                exp = exp + LPVar[abs(formula[i][j])]
        exp = exp >= 1
        prob += exp 

    exp = 0
    for i in range(1, num_vars + 1):
        exp = exp + v[i] * LPVar[i]
    prob += exp
    prob.solve()
    lst = []
    for i in range(1, len(LPVar)):
        lst.append(LPVar[i].varValue)

#    if math.isnan(v_star):
#        return 0
    for i in range(len(lst)):
        try:
            lst[i] = min(float(lst[i]), 1 - float(lst[i]))
        except TypeError:
            print "Type error in LPSlack", sys.argv[1]
            return [0, 0]
    if np.mean(lst) == 0:
        return [0, 0]
    return [np.std(lst) / np.mean(lst), np.mean(lst)]


#--------------------------------------------- Get sat prob feature ------------------------------------------#


def get_sat_prob(formula, num_vars):
    bi_clause_occ_dic = {}
    ter_clause_occ_dic = {}
    var_occ_bi = {}
    var_occ_ter = {}
    for i in range(1, num_vars + 1):
        var_occ_bi[i] = Set()
        var_occ_ter[i] = Set()
    for clause in formula:
        c = get_c_string(clause)
        if len(clause) == 2:
            if c in bi_clause_occ_dic:
                bi_clause_occ_dic[c] += 1
            else:
                bi_clause_occ_dic[c] = 1
            for var in clause:
                var_occ_bi[abs(var)].add(c)
        elif len(clause) == 3:
            if c in ter_clause_occ_dic:
                ter_clause_occ_dic[c] += 1
            else:
                 ter_clause_occ_dic[c] = 1
            for var in clause:
                var_occ_ter[abs(var)].add(c)
    to_return = []
    if len(bi_clause_occ_dic) != 0:        
        lst = []
        for key in bi_clause_occ_dic:
            lst.append(bi_clause_occ_dic[key])
        to_return += add_stat(lst)
        lst = []
        for key in var_occ_bi:
            lst.append(len(var_occ_bi[key])/float(len(bi_clause_occ_dic)))
        to_return += add_stat(lst)
    else:
        lst = [0]
        to_return += add_stat(lst)
        to_return += add_stat(lst)
    if len(ter_clause_occ_dic) != 0:
        lst = []
        for key in ter_clause_occ_dic:
            lst.append(ter_clause_occ_dic[key])
        to_return += add_stat(lst)
        lst = []
        for key in var_occ_ter:
            lst.append(len(var_occ_ter[key])/float(len(ter_clause_occ_dic)))
        to_return += add_stat(lst)
    else:
        lst = [0]
        to_return += add_stat(lst)
        to_return += add_stat(lst)
    return to_return


def get_c_string(clause):
    s = ""
    for i in range(len(clause)):
        clause[i] = abs(clause[i])
    clause.sort()
    for ele in clause:
        s += str(ele) + "-"
    return s[:-1]


#-----------------------------------------------statistics-------------------------------------------------#

def add_stat(lst):
    """
    add max, min, mean, std of the give statistics to the features list.
    """
    return [max(lst),min(lst), np.mean(lst), np.std(lst)]


def add_stat_normalized(lst, num_vars):
    """                                                                        
    Normalized the list with the number of variables; add max, min, mean, std of the give statistics to the features list. 
    """
    for i in range(len(lst)):
        lst[i] = lst[i]/float(num_vars)
    return [max(lst),min(lst), np.mean(lst), np.std(lst)]


if __name__ == "__main__":
    main()
