#include<iostream>
#include<fstream>
#include<string>
#include<map>
#include<set>

using namespace std;
/*
class Arc {
    public:
    Arc(int a, int b, float c) {src=a; dst=b; weight=c; }
    int get_src(){return src;}
    int get_dst() {return dst;}
    int get_weight() {return weight;}\
    void read(fstream &is) {

    }
    private:
    
    int src; int dst; float weight;
};

class Weighted_edge {
    public:
    Weighted_edge(){}
    Weighted_edge(int d, float w){dst=d; weight=w;}
    int get_dst(){return dst;}
    float get_weight(){return weight;}
    void print(){ cout << dst << " " << weight << "\n"; }

    private:
    int dst;float weight;
};*/

class Graph {
    public:
    Graph(string f) {input_file_name = f; current_pos = 0;}
    Graph(int n) {current_pos = 0; }
    void read() {
        input_file.open(input_file_name,ios::in); 
        if (input_file.is_open()){ 
            int s,d; float w;
            input_file >> nbr_of_uedges;

            for (int i=0 ; i<nbr_of_uedges ; i++) {
                pair<int,float> p;
                input_file >> s >> d >> w ; 
                edges[s].insert(make_pair(d,w));
                edges[d].insert(make_pair(s,w));
            }

            input_file.close();
        }  else  cout << "Problem with opening file.\n\n"; 
        cout << "\n *  1/2 graph loaded " << endl; 
        cout << "\n ** 2/2 adjacency list created " << endl << endl; 
    }

    void print() {
        for(map<int,set<pair<int,float>>>::iterator it=edges.begin(); it!=edges.end(); it++) {
            for (set<pair<int,float>>::iterator it2=it->second.begin(); it2!=it->second.end(); it2++) {
                cout << it->first << " " << it2->first << " " << it2->second << "\n";
            }
        }
    }

    private:
    int current_pos, nbr_of_uedges;
    map<int,set<pair<int,float>>> edges;
    string input_file_name;
    fstream input_file;
};

int main(){

    Graph g = Graph("graph_cpp_.txt");
    g.read();
    g.print();
    return 0;
}
