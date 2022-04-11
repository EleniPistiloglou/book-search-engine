#include<iostream>
#include<fstream>
#include<string>
#include<map>
#include<set>
#include<vector>
#include<queue>

using namespace std;


class Graph {
    public:
    Graph(string f) {input_file_name = f; current_pos = 0;}
    Graph(int n) {current_pos = 0; }
    void read() {
        input_file.open(input_file_name,ios::in); 
        if (input_file.is_open()){ 
            int s,d; float w;
            input_file >> nbr_of_uedges;
            nbr_of_uedges_minus_one = nbr_of_uedges-1;

            for (int i=0 ; i<nbr_of_uedges ; i++) {
                pair<int,float> p;
                input_file >> s >> d >> w ; 
                edges[s].insert(make_pair(d,w));
                edges[d].insert(make_pair(s,w));
            }

            input_file.close();
        }  else  cout << "Problem with opening file.\n\n"; 
        nbr_of_nodes = edges.size();
        nbr_of_nodes_minus_one = nbr_of_nodes-1;
        cout << "\n *  1/2 graph loaded " << endl; 
        cout << "\n    " << nbr_of_nodes << " nodes " << endl; 
        cout << "\n ** 2/2 adjacency list created " << endl << endl; 
    }

    void print() {
        for(map<int,set<pair<int,float>>>::iterator it=edges.begin(); it!=edges.end(); it++) {
            for (set<pair<int,float>>::iterator it2=it->second.begin(); it2!=it->second.end(); it2++) {
                cout << it->first << " " << it2->first << " " << it2->second << "\n";
            }
        }
    }

    float dijkstra(int source) {

        float sum=0.0;
        map<int,float> dist;  // keys contained in here are not yet visited
        dist[source] = 0.0;
        map<float, set<int>> invert_dist;   // to find the next node
        invert_dist[0.0].insert(source);
        priority_queue<float, vector<float>, greater<float> > queue;
        queue.push(0.0);
        set<int> seen;
        float new_dist, old_dist, min_weight;
        int current, child;    // current node

        while(!queue.empty()) {

            min_weight = queue.top();   //cout<<"\n\nmin weight: "<<min_weight<<"\n";
            current = *invert_dist[min_weight].begin();  invert_dist[min_weight].erase(current);  if (invert_dist[min_weight].empty()) { invert_dist.erase(min_weight); queue.pop(); } seen.insert(current); 
            //cout<< "\nprocessing " << current << "\n";
            for(set<pair<int,float>>::iterator it=edges[current].begin(); it!=edges[current].end(); it++) {
                child = it->first; 
                if (seen.find(child)!=seen.end()) continue;
                else { //cout<<"child "<<child<<"\n";
                    new_dist = dist[current] + it->second; //cout<<"new "<<new_dist;
                    if (dist.find(child)!=dist.end()) {
                        old_dist = dist[child]; //cout<< "old "<<old_dist<<endl; 
                        if (new_dist < old_dist) {
                            dist[child] = new_dist; 
                            invert_dist[old_dist].erase(child); 
                            invert_dist[new_dist].insert(child); 
                            queue.push(new_dist);  //cout<<"new dist "<<new_dist<<"\n";
                        }
                    } else {
                        dist[child]=new_dist;
                        invert_dist[new_dist].insert(child); 
                        queue.push(new_dist);  //cout<<"new dist "<<new_dist<<"\n";
                    }
                }
            }
        }

        for (map<int,float>::iterator nodes=dist.begin(); nodes!=dist.end(); nodes++) {
            sum += nodes->second; 
        }
        //cout << sum << endl;
        //cout << seen.size() << endl;
        return sum;  
    }

    void centrality() {
        float rank;
        output_rank = "output_rank_"+input_file_name; 
        fstream output_rank_file;
        for (map<int,set<pair<int,float>>>::iterator node=edges.begin(); node!=edges.end(); node++) {
            rank = 1.0 / dijkstra(node->first) * nbr_of_nodes_minus_one;
            output_rank_file.open(output_rank,ios_base::app); 
            if (output_rank_file.is_open()){ 
                output_rank_file << node->first << " " << rank << "\n";
                output_rank_file.close();
            } else cout << "Could not open output file for rank :  " << node->first << " " << rank << "\n";
            rank = 0.0;
            //cout << node->first << endl;
        }     
    }

    private:
    int current_pos, nbr_of_uedges, nbr_of_uedges_minus_one, nbr_of_nodes, nbr_of_nodes_minus_one;
    map<int,set<pair<int,float>>> edges;
    string input_file_name, output_rank;
    fstream input_file;
};

int main(){
    cout << "--------------------------------- FIRST SIMPLE TEST ----------------------------------\n";
    Graph g1 = Graph("graph_cpp.txt");
    g1.read();
    g1.print();
    g1.centrality();
    cout << "--------------------------------------------------------------------------------------\n\n\n";

    cout << "-------------------------------- SECOND   SIMPLE TEST --------------------------------\n";
    Graph g2 = Graph("graph_cpp_8v.txt");
    g2.read();
    g2.print();
    g2.centrality();
    cout << "--------------------------------------------------------------------------------------\n\n\n";

    cout << "--------------------------------- REAL DATA TEST 7 -----------------------------------\n";
    Graph g5 = Graph("graph_cpp_07_w0.txt");
    g5.read();
    g5.centrality();
    cout << "--------------------------------------------------------------------------------------\n\n\n";

    cout << "--------------------------------- REAL DATA TEST 5 -----------------------------------\n";
    Graph g5 = Graph("graph_cpp_05_w0.txt");
    g5.read();
    g5.centrality();
    cout << "--------------------------------------------------------------------------------------\n\n\n";

    cout << "--------------------------------- REAL DATA TEST 3 -----------------------------------\n";
    Graph g3 = Graph("graph_cpp_03_w0.txt");
    g3.read();
    g3.centrality();
    cout << "--------------------------------------------------------------------------------------\n\n\n";

    return 0;
}
