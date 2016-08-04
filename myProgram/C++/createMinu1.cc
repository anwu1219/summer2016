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
using namespace std;

vector<vector<int>> cur_formula = vector<vector<int>>();
set<int> unassigned = set<int>();
void write_SAT(string& filename, vector<vector<int>> formula);
vector<vector<int>> unit_propagation(vector<vector<int>> formula);
vector<vector<int>> tempFormula(vector<vector<int>> formula, int lit);
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
  for (int lit = 1; lit <= 1; lit++){
    temp = tempFormula(formula, lit);
    outputFile.open(string(filename + "_" + to_string(lit) + ".dimacs").c_str());
    outputFile << "c generated" << endl;
    outputFile << "p cnf " << num_var - 1 << " " << temp.size() << endl;
    for (auto& line : temp){
      for (auto& ele : line) {
	if (abs(ele) > lit) outputFile << ele / abs(ele) * (abs(ele) - 1) << " ";
	else outputFile << ele << " ";
      }
      outputFile << "0" << endl; 
    }
    outputFile.close();
    outputFile.clear(); // clear flags
    temp = tempFormula(formula, -lit);
    outputFile.open(string(filename + "_" + to_string(-lit) + ".dimacs").c_str());
    outputFile << "c generated" << endl;
    outputFile << "p cnf " << num_var - 1 << " " << temp.size() << endl;
    for (auto& line : temp){
      for (auto& ele : line) {
	if (abs(ele) > lit) outputFile << ele / abs(ele) * (abs(ele) - 1) << " ";
	 else outputFile << ele << " ";
      }
      outputFile << "0" << endl;
    }
    outputFile.close();
    outputFile.clear(); 
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

  std::vector<std::vector<int>> tempFormula(vector<vector<int>> cur_formula, int lit){
    vector<vector<int>> temp_formula;
    for (auto &line : cur_formula){
      vector<int> temp_line;
      for (auto &ele : line){
	if (ele == lit){
	  temp_line.push_back(0);
	  break;
	} else if (ele != -lit) temp_line.push_back(ele);
      }
      if (temp_line.empty()){
	vector<vector<int>> conflict_formula;
	conflict_formula.push_back({0});
	return conflict_formula;
      }
      else if (temp_line.back() != 0) temp_formula.push_back(temp_line);
    }
    return temp_formula;
    //    return unit_propagation(temp_formula);
  }

  std::vector<std::vector<int>> unit_propagation(std::vector<std::vector<int>> formula){
    for (auto &line : formula){
      if (line.size() == 1){
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
	return unit_propagation(t_formula);
      }
    }
    //  formula.push_back({num_var});
    return formula;
  }
