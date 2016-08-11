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

vector<vector<int>> cur_formula = vector<vector<int>>();
set<int> unassigned = set<int>();
void write_SAT(string& filename, vector<vector<int>> formula);
std::vector<std::vector<int>> unit_propagation(std::vector<std::vector<int>>& formula, int& cur_num_var);
std::vector<std::vector<int>> tempFormula(const std::vector<std::vector<int>>& cur_formula, int lit, bool propagation, int& cur_num_var);
vector<string> split(string str, char delimiter);
const bool READ_SOL_ORDER = true;

int main(int argc, char *argv[]){
  string line_s;
  string original_cnf = split(argv[1], '.')[0];
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
  myfile.close();
  write_SAT(original_cnf, formula);
  return 0;
}


void write_SAT(string& filename, vector<vector<int>> formula){
  int num_var = 300;
  vector<vector<int>> temp;
  ofstream outputFile;
  std::vector<int> vars;
  for (int i = 1; i <= num_var; i++) vars.push_back(i);
  std::vector<double> f;
  std::random_device rd;
  std::mt19937 g(rd());
  int i, lit, cur_num_var;
  int NUM_TRIALS = 200;
  for (int index = 0; index < NUM_TRIALS; index++){
    cur_num_var = num_var;
    std::shuffle(vars.begin(), vars.end(), g); i = 0;
    lit = rand() % 2 == 1 ? (vars[i++]) : (- vars[i++]);
    temp = tempFormula(formula, lit, false, cur_num_var);
    while (cur_num_var >= 0.92 * num_var) {
      lit = rand() % 2 == 1 ? (vars[i++]) : (- vars[i++]);
      temp = tempFormula(temp,lit, true, cur_num_var);
      if (temp[0].size() == 1 && temp[0][0] == 0) break;
    }
    if (temp[0].size() == 1 && temp[0][0] == 0) continue;
    map<int, int> new_vars;
    for (auto& line : temp) for (auto& ele : line) if (new_vars.find(abs(ele)) == new_vars.end()) new_vars[abs(ele)] = new_vars.size();
    outputFile.open(string(filename + "_" + to_string(index) + ".dimacs").c_str());
    outputFile << "c generated" << endl;
    outputFile << "p cnf " << new_vars.size() << " " << temp.size() << endl;
    for (auto& line : temp){
      for (auto& ele : line) outputFile << abs(ele) / ele * new_vars[abs(ele)] << " ";
      outputFile << "0" << endl; 
    }
    outputFile.close();
    outputFile.clear(); // clear flags
  }
}



    //---------------------------------------------------------- Helper methods ---------------------------------------------------------//
vector<string> split(string str, char delimiter) {
  vector<string> internal;
  stringstream ss(str); // Turn the string into a stream.                                                                                                                   
  string tok;
  while(getline(ss, tok, delimiter)) {
    internal.push_back(tok);
  }
  return internal;
}


std::vector<std::vector<int>> tempFormula(const std::vector<std::vector<int>>& cur_formula, int lit, bool propagation, int& cur_num_var){
  std::vector<std::vector<int>> temp_formula;
  cur_num_var--;
  for (unsigned int i = 0; i < cur_formula.size(); i++){
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
  if (propagation) return unit_propagation(temp_formula, cur_num_var);
  return temp_formula;
}



std::vector<std::vector<int>> unit_propagation(std::vector<std::vector<int>>& formula, int& cur_num_var){
  for (auto &line : formula){
    if (line.size() == 1){
      int lit = line[0];
      cur_num_var--;
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
      return unit_propagation(t_formula, cur_num_var);
    }
  }
  return formula;
}
