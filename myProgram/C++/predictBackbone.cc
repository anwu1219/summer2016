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
#include <sstream>
#include <algorithm>

using namespace std;


double logistics(std::vector<double>& feats);
set<int> unassigned = set<int>();
string clause_string_sign(vector<int> clause);
string clause_string(vector<int> clause);
vector<double> getFeatures(vector<vector<int>>& formula, unsigned int num_var, unsigned int num_clause);
void LP_features(vector<vector<int>>& formula, set<int> local_unassigned, int num_eles, vector<double>& feats);
void add_stat_mean_var(vector<double>& lst, vector<double>& feats);
void add_stat_all(vector<double>& lst, vector<double>& feats);
vector<vector<int>> unit_propagation(vector<vector<int>> formula, int num_var);
std::vector<std::vector<int>> tempFormula(const std::vector<std::vector<int>>& cur_formula, int lit, bool propagation);
vector<string> split(string str, char delimiter);
void predict(const std::vector<std::vector<int>> cur_formula);
const vector<double> coefs = {16.467835621478716, -0.7214383258403004, 70.99255789910569, -7.173878987379937, -6.184148527357918, -1.5245047240000686, -0.00866101515362342, -8.977260522739645, 32.0074577386339, 27.908048273907983};
const double intercept = -71.5403837;

vector<string> split(string str, char delimiter) {
  vector<string> internal;
  stringstream ss(str); // Turn the string into a stream.                                                                                                                                    
  string tok;

  while(getline(ss, tok, delimiter)) {
    internal.push_back(tok);
  }
  return internal;
}


int main(int argc, char *argv[]){
  string line_s;
  ifstream myfile (argv[1]);
  int counter = 0;
  vector<vector<int>> formula;
  vector<string> line;
  vector<int> temp;
  unsigned int num_vars = 0;
  unsigned int num_clauses = 0;
  if (myfile.is_open()){
    while(getline(myfile,line_s)){ // To get you all the lines.
      line = split(line_s, ' ');
      if (line[0].compare("p") == 0){
        num_vars = atoi(line[2].c_str());
        if (atoi(line[3].c_str()) != 0) num_clauses = atoi(line[3].c_str());
        else num_clauses = atoi(line[4].c_str());
      }
      else if (line[0].compare("c") != 0){
        temp = vector<int>();
        for (unsigned int i = 0; i < line.size() - 1; i++) if (atoi(line[i].c_str()) != 0) temp.push_back(atoi(line[i].c_str()));
        formula.push_back(temp);
      }
    }
  }
  formula.push_back({int(num_vars)});
  predict(formula);
  return 0;
}


void predict(const std::vector<std::vector<int>> cur_formula){
  std::vector<int> vars;
  for (int i = 0; i < cur_formula.back()[0]; i++) vars.push_back(i);
  std::vector<std::vector<int>> temp, cur_temp;
  std::vector<double> f;
  std::random_device rd;
  std::mt19937 g(rd());
  int i, lit;
  double sum, prob_sum, prob;
  int NUM_TRIALS = 100;
  for (int first_lit = 0; first_lit < cur_formula.back()[0]; first_lit++){
    cur_temp = tempFormula(cur_formula, first_lit + 1, false);
    prob_sum = 0;
    for (int index = 0; index < NUM_TRIALS; index++){
      std::shuffle(vars.begin(), vars.end(), g); i = 0;
      lit = rand() % 2 == 1 ? (1 + vars[i++]) : ( -1 - vars[i++]);
      temp = tempFormula(cur_temp, lit, true);
      while (temp.back()[0] > 0.96 * cur_formula.back()[0]) {
	lit = rand() % 2 == 1 ? (1 + vars[i++]) : (-1 - vars[i++]);
	if (abs(lit) == first_lit) continue;
	temp = tempFormula(temp,lit, true);
	if (temp.empty() || (temp[0].size() == 1 && temp[0][0] != 0)) break;
	if (temp[0].size() == 1 && temp[0][0] == 0) break;
      }
      if (temp.empty() || (temp[0].size() == 1 && temp[0][0] != 0)){
	prob_sum++;
	continue;
      }
      if (temp[0].size() == 1 && temp[0][0] == 0) continue;
      f = getFeatures(temp, temp.back()[0], temp.size() - 1);
      sum = logistics(f);
      prob_sum += 1 / (1 + exp(-1 * sum));
    }
    prob = prob_sum / NUM_TRIALS;
    if (prob < 0.5) cout << -first_lit << " is a backbone" << endl;
    else cout << first_lit << "is no a backbone" << endl;
  }
}


std::vector<std::vector<int>> tempFormula(const std::vector<std::vector<int>>& cur_formula, int lit, bool propagation){
  std::vector<std::vector<int>> temp_formula;
  for (unsigned int i = 0; i < cur_formula.size() - 1; i++){
    auto line = cur_formula[i];
    std::vector<int> temp_line;
    for (auto &ele : line){
      if (ele == lit){
        temp_line.push_back(0);
        break;
      } else if (ele != -lit) temp_line.push_back(ele);
    }
    if (temp_line.empty()){
      std::vector<std::vector<int>> conflict_formula;
      conflict_formula.push_back({0});
      return conflict_formula;
    }
    else if (temp_line.back() != 0) temp_formula.push_back(temp_line);
  }
  if (propagation) return unit_propagation(temp_formula, cur_formula.back()[0] - 1);
  int num_var = cur_formula[cur_formula.size()-1][0] - 1;
  temp_formula.push_back({num_var});
  return temp_formula;
}


std::vector<std::vector<int>> unit_propagation(std::vector<std::vector<int>> formula, int num_var){
  for (auto &line : formula){
    if (line.size() == 1){
      num_var--;
      int lit = line[0];
      std::vector<std::vector<int>> t_formula;
      for (auto & line : formula){
	std::vector<int> temp_line;
        for (auto &ele : line){
          if (ele == lit){
            temp_line.push_back(0);
            break;
          } else if (ele != -lit){
            temp_line.push_back(ele);
          }
        }
        if (temp_line.empty()){
	  std::vector<std::vector<int>> conflict_formula;
          conflict_formula.push_back({0});
          return conflict_formula;
        }
        else if (temp_line.back() != 0) t_formula.push_back(temp_line);
      }
      return unit_propagation(t_formula, num_var);
    }
  }
  formula.push_back({num_var});
  return formula;
}


double logistics(std::vector<double>& feats){
  double sum = intercept;
  assert(feats.size() == coefs.size());
  for (unsigned int j = 0; j < feats.size(); j++) sum += feats[j] * coefs[j];
  return sum;
}



std::vector<double> getFeatures(std::vector<std::vector<int>>& formula, unsigned int num_var, unsigned int num_clause) {
  std::vector<double> feats, pos_neg_ratios, pos_neg_occ;
  std::map<unsigned int, std::vector<int>> pos_neg_occurence;
  std::set<std::string> bi_clause_occ, ter_clause_occ;
  std::set<std::string> all_clauses;
  std::map<int, std::set<std::string>> var_occ_bi, var_occ_ter;
  std::set<int> local_unassigned;
  double num_ter, num_horn, num_rev_horn, POSNEG_ratio_var_mean;
  unsigned int pos_num, size, pos_occ, var_occ, bi_clause, ter_clause, num_eles;
  num_ter = 0; num_horn = 0; num_rev_horn = 0; POSNEG_ratio_var_mean = 0;
  bi_clause = 0;   ter_clause = 0; num_eles = 0;
  for (unsigned int i = 0; i < formula.size() - 1; i++){
    auto clause = formula[i];
    std::string c_sign = clause_string_sign(clause);
    size = clause.size();
    num_eles += size;
    if (all_clauses.find(c_sign) == all_clauses.end()) all_clauses.insert(c_sign);
    else {
      num_clause--;
      continue;
    }
    std::string c = clause_string(clause);
    pos_num = 0;
    if (size == 3) num_ter++;
    for (auto &lit : clause){
      if (local_unassigned.find(abs(lit)) == local_unassigned.end()) local_unassigned.insert(abs(lit));
      if (lit > 0) pos_num++;
      if (pos_neg_occurence.find(abs(lit)) == pos_neg_occurence.end()) pos_neg_occurence[abs(lit)] = {0,0};
      pos_neg_occurence[abs(lit)][0]++;
      if (lit > 0) pos_neg_occurence[abs(lit)][1]++;
      if (size == 2){
        if (var_occ_bi.find(abs(lit)) == var_occ_bi.end()) var_occ_bi[abs(lit)] = std::set<std::string>();
        var_occ_bi[abs(lit)].insert(c);
      } else if (size == 3){
        if (var_occ_ter.find(abs(lit)) == var_occ_ter.end()) var_occ_ter[abs(lit)] = std::set<std::string>();
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
  add_stat_mean_var(pos_neg_ratios, feats); // pos_neg_cl_ratio                                                                                                                                                                                                                                                            
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
  return feats;
}



string clause_string_sign(std::vector<int> clause){
  std::vector<int> sort_clause;
  for (auto& lit : clause) sort_clause.push_back(lit);
  std::sort(sort_clause.begin(),sort_clause.end());
  std::string s = "";
  for (auto& var : sort_clause) s += std::to_string(var) + "-";
  return s;
}



string clause_string(std::vector<int> clause){
  std::vector<int> sort_clause;
  for (auto& lit : clause) sort_clause.push_back(abs(lit));
  std::sort(sort_clause.begin(),sort_clause.end());
  std::string s = "";
  for (auto& var : sort_clause) s += std::to_string(var) + "-";
  return s;
}


void add_stat_mean_var(std::vector<double>& lst, std::vector<double>& feats){
  // Get the max, min, mean, std of the lst and append it to feats                                                                                                                           
  double sum = std::accumulate(lst.begin(), lst.end(), 0.0);
  double mean = sum / lst.size();
  std::vector<double> diff(lst.size());
  std::transform(lst.begin(), lst.end(), diff.begin(), [mean](double x) { return x - mean; });
  double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);
  double stdev = std::sqrt(sq_sum / lst.size());
  feats.push_back(mean);
  feats.push_back(stdev);
}



void add_stat_all(std::vector<double>& lst, std::vector<double>& feats){
  // Get the max, min, mean, std of the lst and append it to feats                                                                                                                           
  double sum = accumulate(lst.begin(), lst.end(), 0.0);
  double mean = sum / lst.size();
  std::vector<double> diff(lst.size());
  std::transform(lst.begin(), lst.end(), diff.begin(), [mean](double x) { return x - mean; });
  double sq_sum = std::inner_product(diff.begin(), diff.end(), diff.begin(), 0.0);
  double stdev = std::sqrt(sq_sum / lst.size());
  auto min_max = std::minmax_element(lst.begin(), lst.end());
  feats.push_back(lst[min_max.second - lst.begin()]);
  feats.push_back(lst[min_max.first - lst.begin()]);
  feats.push_back(mean);
  feats.push_back(stdev);
}
