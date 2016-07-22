/***************************************************************************************[Solver.cc]
Copyright (c) 2003-2006, Niklas Een, Niklas Sorensson
Copyright (c) 2007-2010, Niklas Sorensson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
**************************************************************************************************/

#include <math.h>
#include <string>
#include <iostream>
#include <fstream>
#include <map>
#include <assert.h>
#include <set>
#include <vector>
#include <queue>
#include <random>
#include "ClpSimplex.hpp"
using namespace std;

const vector<double> coefs = {-3.86515851e+00, 2.83465926e+00, 9.87928376e-02, -5.86586537e+00, 6.03585822e+00, 2.71703339e+00, 2.21661857e+00, 5.36610803e-01, -8.05975610e-02, -6.11138941e-01, 2.65656900e+00, 3.44573920e+00, -2.13359550e-06, -2.17445095e+01, 4.07360084e+00, 3.01420109e-01, -1.45283106e+00, 1.20557309e+01, -8.25112203e+00,  5.59772461e+00, -2.85966541e+00,  -4.29953825e+00};
const double intercept = 9.22652748;

vector<vector<int>> cur_formula = vector<vector<int>>();
set<int> unassigned = set<int>();
string clause_string_sign(vector<int> clause);
string clause_string(vector<int> clause);
vector<double> getFeatures(vector<vector<int>>& formula, unsigned int num_var, unsigned int num_clause);
void LP_features(vector<vector<int>>& formula, set<int> local_unassigned, int num_eles, vector<double>& feats);
void add_stat_mean_var(vector<double>& lst, vector<double>& feats);
void add_stat_all(vector<double>& lst, vector<double>& feats);



int main(int argc, char *argv[]){
  string line;
  ifstream myfile (argv[1]);
  if (myfile.is_open())
    {
      while(getline(myfile,line))
	{
	  cout << line << '\n';
	}
      myfile.close();
    }
  return 0;
}


vector<double> getFeatures(vector<vector<int>>& formula, unsigned int num_var, unsigned int num_clause) {
  vector<double> feats, pos_neg_ratios, pos_neg_occ;
  map<unsigned int, vector<int>> pos_neg_occurence;
  set<string> bi_clause_occ, ter_clause_occ;
  set<string> all_clauses;
  map<int, set<string>> var_occ_bi, var_occ_ter;
  set<int> local_unassigned;
  double num_bi, num_ter, num_horn, num_rev_horn, POSNEG_ratio_var_mean;
  unsigned int pos_num, size, pos_occ, var_occ, bi_clause, ter_clause, num_eles;
  num_bi = 0; num_ter = 0; num_horn = 0; num_rev_horn = 0; POSNEG_ratio_var_mean = 0; 
  bi_clause = 0;   ter_clause = 0; num_eles = 0;
  for (unsigned int i = 0; i < formula.size() - 1; i++){
    auto clause = formula[i];
    string c_sign = clause_string_sign(clause);
    size = clause.size();
    num_eles += size;
    if (all_clauses.find(c_sign) == all_clauses.end()) all_clauses.insert(c_sign);
    else {
      num_clause--;
      continue;
    }
    string c = clause_string(clause);
    pos_num = 0;
    if (size == 2) num_bi++;
    if (size == 3) num_ter++;
    for (auto &lit : clause){
      if (local_unassigned.find(abs(lit)) == local_unassigned.end()) local_unassigned.insert(abs(lit));
      if (lit > 0) pos_num++;
      if (pos_neg_occurence.find(abs(lit)) == pos_neg_occurence.end()) pos_neg_occurence[abs(lit)] = {0,0};
      pos_neg_occurence[abs(lit)][0]++;
      if (lit > 0) pos_neg_occurence[abs(lit)][1]++;
      if (size == 2){
	if (var_occ_bi.find(abs(lit)) == var_occ_bi.end()) var_occ_bi[abs(lit)] = set<string>();
	var_occ_bi[abs(lit)].insert(c);
      } else if (size == 3){
	if (var_occ_ter.find(abs(lit)) == var_occ_ter.end()) var_occ_ter[abs(lit)] = set<string>();
	var_occ_ter[abs(lit)].insert(c);
      }
    }
    if (pos_num <= 1) num_horn++;
    if (size - pos_num <= 1) num_rev_horn++;
    pos_neg_ratios.push_back(double(pos_num) / size);
    if (size == 2){
      if (bi_clause_occ.find(c) == bi_clause_occ.end()){
	bi_clause_occ.insert(c);
	bi_clause++;
      }
    } else if (size == 3){
      if (ter_clause_occ.find(c) == ter_clause_occ.end()){
	ter_clause_occ.insert(c);
	ter_clause++;
      }
    }
  }
  feats.push_back(double(num_clause) / num_var);
  add_stat_mean_var(pos_neg_ratios, feats); // pos_neg_cl_ratio
  feats.push_back(double(num_bi) / num_clause); //rat_bi    
  feats.push_back(double(num_ter) / num_clause); //rat_ter  
  feats.push_back(num_horn / num_clause); //rat_horn
  feats.push_back(num_rev_horn / num_clause); //rat_rev_horn
  for(auto const &occ : pos_neg_occurence){
    pos_occ = occ.second[1];
    var_occ = occ.second[0];
    pos_neg_occ.push_back(double(pos_occ)/var_occ);
    double temp = 0.5 - pos_occ / double(var_occ);
    POSNEG_ratio_var_mean += temp > 0 ? temp : -temp;
  }
  add_stat_all(pos_neg_occ, feats); // pos_neg_ratio
  feats.push_back(POSNEG_ratio_var_mean * 2 / num_var); // POSNEG_ratio
  LP_features(formula, local_unassigned, num_eles, feats); //LP_feats
  if (bi_clause == 0){
    vector<double> n = {0};
    add_stat_all(n, feats);
  } else{
    vector<double> var_occ_bi_ratio;
    for (auto& key : var_occ_bi) var_occ_bi_ratio.push_back(key.second.size() / double(bi_clause));
    for (unsigned i = 0; i < local_unassigned.size() - var_occ_bi.size(); i++) var_occ_bi_ratio.push_back(0);
    add_stat_all(var_occ_bi_ratio, feats);
  }
  if (ter_clause == 0){
    vector<double> n = {0};
    add_stat_all(n, feats);
  } else{
    vector<double>var_occ_ter_ratio;
    for(auto& key : var_occ_ter) var_occ_ter_ratio.push_back(key.second.size() / double(ter_clause));
    for(unsigned i = 0; i < local_unassigned.size() - var_occ_ter.size(); i++) var_occ_ter_ratio.push_back(0);
    add_stat_all(var_occ_ter_ratio, feats);
  }
  return feats;
}

void LP_features(vector<vector<int>>& formula, set<int> local_unassigned, int num_eles, vector<double>& feats){
  ClpSimplex modelByRow;
  map<int, int> vars;
  int j = 0;
  for (auto& var: local_unassigned){
    vars[var] = j;
    vars[-var] = j;
    j++;
  }
  int numberRows = formula.size() - 1;
  int numberColumns = local_unassigned.size();

  double objective [numberColumns]; //done
  double columnLower [numberColumns]; //done
  double columnUpper [numberColumns]; //done
  double rowLower [numberRows]; //done
  int rowStart [numberRows + 1]; //done
  int column [num_eles]; //done
  double elementByRow [num_eles]; //done

  for (int i = 0; i < numberColumns; i++){
    columnLower[i] = 0;
    columnUpper[i] = 1;
    objective[i] = 0;
  }
  int index = 0;
  int lower_bound;
  for (int i = 0; i < numberRows; i++){
    rowStart[i] = index;
    lower_bound = 1;
    for (auto& lit : formula[i]){
      column[index] = vars[lit];
      if (lit > 0) {
	elementByRow[index] = 1;
	objective[vars[lit]]--; // try to maximize
      } else {
	elementByRow[index] = -1;
	lower_bound--;
	objective[vars[lit]]++;
      }
      index++;
    }
    rowLower[i] = lower_bound;
  } 
  assert(index == num_eles);
  rowStart[numberRows] = num_eles;
  int numberElements = rowStart[numberRows];
  CoinPackedMatrix byRow(false, numberColumns, numberRows, numberElements, elementByRow, column, rowStart, NULL);
  modelByRow.loadProblem(byRow, columnLower, columnUpper, objective, rowLower, NULL);
  modelByRow.setLogLevel(0);
  modelByRow.initialSolve();
  double * solution = modelByRow.primalColumnSolution();
  double sum = 0.0;
  double mean =0.0;
  double var =0.0;
  for (int i = 0; i < numberColumns; i++){
    solution[i] =  solution[i] < 1 - solution[i] ? solution[i] : 1 - solution[i];
    sum += solution[i];
  }
  mean = sum / double(numberColumns);
  if (std::isnan(mean) || mean == 0){
    feats.push_back(0);
    feats.push_back(0);
  } else {
    sum = 0;
    for (int i = 0; i < numberColumns; i++) sum += pow((solution[i] - mean), 2);
    var = sqrt(sum / double(numberColumns));
    feats.push_back(var / mean);
    feats.push_back(mean);
  }
}

string clause_string_sign(vector<int> clause){
  vector<int> sort_clause;
  for (auto& lit : clause) sort_clause.push_back(lit);
  sort(sort_clause.begin(),sort_clause.end());
  string s = "";
  for (auto& var : sort_clause) s += to_string(var) + "-";
  return s;
}


string clause_string(vector<int> clause){
  vector<int> sort_clause;
  for (auto& lit : clause) sort_clause.push_back(abs(lit));
  sort(sort_clause.begin(),sort_clause.end());
  string s = "";
  for (auto& var : sort_clause) s += to_string(var) + "-";
  return s;
}

void add_stat_mean_var(vector<double>& lst, vector<double>& feats){
  // Get the max, min, mean, std of the lst and append it to feats
  double sum = 0.0;
  double mean =0.0;
  double var =0.0;
  for (auto &i : lst){
    sum += i;
  }
  mean = sum / double(lst.size());
  sum = 0;
  for (auto &i : lst) sum += pow((i - mean), 2);
  var = sqrt(sum / double(lst.size()));
  feats.push_back(mean);
  feats.push_back(var);
}

void add_stat_all(vector<double>& lst, vector<double>& feats){
  // Get the max, min, mean, std of the lst and append it to feats                                    
  double sum = 0.0;
  double mean =0.0;
  double var =0.0;
  double min = 9999999;
  double max = -9999999;
  for (auto &i : lst){
    if (i < min) min = i;
    if (i > max) max = i;
    sum += i;
  }
  mean = sum / double(lst.size());
  sum = 0;
  for (auto &i : lst) sum += pow((i - mean), 2);
  var = sqrt(sum / double(lst.size()));
  feats.push_back(max);
  feats.push_back(min);
  feats.push_back(mean);
  feats.push_back(var);
}

