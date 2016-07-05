import copy
import sys
sys.path.append("/Library/Python/2.7/site-packages")
import community
import networkx as nx
import numpy as np
import scipy as sp
import math
from pulp import *


def choose_lit(filename, solution, num_vars):
    content = []
    with open(filename, 'r') as in_file: # Read a dimacs file
        for line in in_file:
            if line[0] == 'c':
                pass
            elif len(content) >= 2:
                content.append(map(int, line.split()))
            else:
                content.append('c generated dimacs file\n')
                content.append(line.split())
    solution = map(int, solution.split());
    return len(write_SAT_file(content, solution, num_vars))


#------------------------------------------------------Generate formula Helper method--------------------------------------------------------#


def write_SAT_file(in_content, solution, num_vars):
    all_vars = range(1, num_vars + 1);
    print solution
    if len(solution) > 0:
        new_dimacs, solution, all_vars = update_content(in_content, solution, 0,  all_vars)
        print "I'm here"
        new_dimacs, solution, all_vars = unit_propagation(new_dimacs, solution, all_vars)
        new_dimacs, solution, all_vars = shrink_formula(new_dimacs, solution, all_vars)
    else:
        new_dimacs = in_content
        all_vars = all_vars
    graphs = []
    for var in all_vars:
        new_dimacs_p, solution_p, all_vars_p = update_content(copy.deepcopy(new_dimacs),[var], 0, copy.deepcopy(all_vars))
        new_dimacs_p, solution_p, all_vars_p = unit_propagation(new_dimacs_p, solution_p, all_vars_p)
        new_dimacs_p, solution_p, all_vars_p = shrink_formula(new_dimacs_p, solution_p, all_vars_p)
        graphs.append(get_features(new_dimacs_p[1:]))
        new_dimacs_n, solution_n, all_vars_n = update_content(copy.deepcopy(new_dimacs),[-var], 0, copy.deepcopy(all_vars))
        new_dimacs_n, solution_n, all_vars_n = unit_propagation(new_dimacs_n, solution_n, all_vars_n)
        new_dimacs_n, solution_n, all_vars_n = shrink_formula(new_dimacs_n, solution_n, all_vars_n)
        graphs.append(get_features(new_dimacs_n[1:]))

    return graphs


def update_content(content, solution, index, all_vars):
    lit = solution[index]
    solution.remove(lit)
    all_vars.remove(abs(lit))
    deleted_clause = 0
    new_dimacs = [content[0],[]]
    for line in content[2:]:
        if lit not in line:
            if -lit in line:
                line.remove(-lit)
            line = update_line(line, abs(lit))
            new_dimacs.append(line)
        else:
            deleted_clause += 1
    info = content[1]
    info[2] = int(info[2]) - 1
    info[3] = int(info[3]) - deleted_clause
    new_dimacs[1] = info  # update the number of clauses                                                                                        
    solution = update_sol(solution, abs(lit))
    all_vars = update_sol(all_vars, abs(lit))
    return new_dimacs, solution, all_vars

def update_sol(solution, var):
    for i in range(len(solution)):
        if abs(solution[i]) > var:
            sign = solution[i] / abs(solution[i])
            solution[i] = sign * (abs(solution[i])-1)
    return solution


def update_line(line, var):
    """                                                                                                                                        
    decrease the numbers of variables by 1                                                                                                     
    """
    for i in range(len(line)):
        if abs(line[i]) > var:
            sign = line[i] / abs(line[i])
            line[i] = sign * (abs(line[i]) - 1)
    return line


def unit_propagation(content, solution, all_vars):
    for i in range(2, len(content)):
        if len(content[i]) == 2:
            lit = content[i][0]
            deleted_clause = 0
            new_dimacs = [content[0],[]]
            for line in content[2:]:
                if lit not in line:
                    if -lit in line:
                        line.remove(-lit)
                    new_dimacs.append(line)
                else:
                    deleted_clause += 1
            for j in range(2, len(new_dimacs)):
                new_dimacs[j] = update_line(new_dimacs[j], abs(lit))
            if lit in solution:
                solution.remove(lit)
            else:
                pass
                #print "Can't find", lit                                                                                              
            if abs(lit) in all_vars:
                all_vars.remove(abs(lit))
            else:
                pass
                #print "Can't find", lit     
            solution = update_sol(solution, abs(lit))
            all_vars = update_sol(all_vars, abs(lit))
            info = content[1]
            info[2] = int(info[2]) - 1
            info[3] = int(info[3]) - deleted_clause
            new_dimacs[1] = info # update the number of clauses                                                                                 
            return unit_propagation(new_dimacs, solution, all_vars)
    return content, solution, all_vars

    
def shrink_formula(content, solution, all_vars):
    for ele in range(len(solution)+1)[1:]:
        if (not any(-ele in line for line in content[2:])) and (not any(ele in line for line in content[2:])):
            for i in range(2, len(content)):
                content[i] = update_line(content[i], abs(ele))
            try:
                if ele in solution:
                    solution.remove(ele)
                else:
                    solution.remove(-ele)
            except ValueError:
                pass;
            try:
                if ele in all_vars:
                    all_vars.remove(ele)
                else:
                    all_vars.remove(-ele)
            except ValueError:
                pass;
            solution = update_sol(solution, abs(ele))
            all_vars = update_sol(all_vars, abs(ele))
            content[1][2] -= 1
            return shrink_formula(content, solution, all_vars)
    return content, solution, all_vars


def contains_empty(content):
    for ele in content[2:]:
        if len(ele) == 1:
            return True
    return False

#----------------------------------------------------------Get features helper method --------------------------------------------------------#


def get_features(content):
    #Computing formula features
    parameters = content[0]
    formula = content[1:] # The clause part of the dimacs file                                                                                  
    num_vars = int(parameters[2]) # AW Number of variables                                                                                      
    if num_vars == 0:
        return
    num_clause = int(parameters[3]) # AW Number of variables                                                                                    
    if num_clause == 0:
        return
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
    features += add_stat_normalized(VIG.degree().values(), num_vars) # VIG degree features                                                      
    # print "4-8 VCG var degree features", add_stat(VCG.degree().values()[:num_vars])                                                           
    features += add_stat_normalized(VCG.degree().values()[:num_vars], num_vars)  # VCG var degree features                                      
    # print "9-13 VCG clause degree features", add_stat(VCG.degree().values()[num_vars:])                                                       
    features += add_stat_normalized(VCG.degree().values()[num_vars:], num_vars)  # VCG clause degree features                                   
    # print "18-20 Occurence of positive and negative literals in each clause", add_stat(get_pos_neg_ratio(formula))[2:]                        
    features += add_stat(get_pos_neg_ratio(formula))[2:]    # Occurence of positive and negative literals in each clause                        
    # print "26-27 Ratio of binary clause", get_binary(formula, num_clause)                                                                     
    features += get_binary(formula, num_clause)   # Ratio of binary clause                                                                      
    # print "28/-28 29-33/ -29-33 Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features", horn_features(formula, num_v\ars, num_clause)
    features += horn_features(formula, num_vars, num_clause) # Ratio_horn, ratio_rev_horn, horn variable features, rev_horn variable features   
    # print "Modularities of VIG & VCG", get_modularities(VIG, VCG, graphic = False)                                                            
    # print "21-25 Occurence of positive and negative literals for each variable", add_stat(get_pos_neg_occ(formula, num_vars))                 
    features += get_pos_neg_occ(formula, num_vars)   # Occurence of positive and negative literals for each variable                            
    features += get_modularities(VIG, VCG, graphic = False) # Modularities of VIG & VCG                                                         
    features += get_LPSLACK_coeff_variation(formula, num_vars, num_clause)
    return features

def preprocess_VIG(formula, VIG):
    """                                                                                                                                                               
    Transforms a formula into int matrix                                                                                                                              
    Builds VIG.                                                                                                                                                       
    """
    for cn in range(len(formula)):
        formula[cn] = formula[cn][:-1]
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
            POSNEG_ratio_var_mean += abs((0.5 - dic[i][1]) / dic[i][0])
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
    Get the ratiotion of horn clauses, reverse horn clauses in the formula,                                                                                            
        print "I'm here"    as well as the occurence of each variable in horn clauses and reverse horn clauses                                                                                 
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
    # solve the problem                                                                                                                                                
    #print LpStatus[status]                                                                                                                                            
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

