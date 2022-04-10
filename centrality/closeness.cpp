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
  
     void centrality(float md) {
        float rank;
        max_distance = md;
        fstream output_rank_file;
        for (map<int,set<pair<int,float>>>::iterator node=edges.begin(); node!=edges.end(); node++) {
            rank = 1.0 / dijkstra(node->first) * nbr_of_uedges_minus_one;
            output_rank_file.open(output_rank,ios::out); 
            if (output_rank_file.is_open()){ 
                output_rank_file << node->first << " " << rank << "\n";
                output_rank_file.close();
            } else cout << "Could not open output file for rank :  " << node->first << " " << rank << "\n";
            rank = -1;
        }
            
    }

    private:

    float dijkstra(int source) {
      
        float sum=0.0;
        map<int,float> dist;  // keys contained in here are not yet visited
        dist[source] = 0.0;
        map<float, set<int>> invert_dist;   // to find the next node
        invert_dist[0.0].insert(source);
        priority_queue<float> queue;  
        queue.push(0.0);
        set<int> seen;
        float new_dist, old_dist, min_weight;
        int current, child;    // current node
      
        while(!queue.empty()) {
          
            min_weight = queue.top();   
            current = *invert_dist[min_weight].begin();  invert_dist[min_weight].erase(current);  if (invert_dist[min_weight].empty()) { invert_dist.erase(min_weight); queue.pop(); } seen.insert(current); cout<< "processing " << current << "\n";
            for(set<pair<int,float>>::iterator it=edges[current].begin(); it!=edges[current].end(); it++) {
                child = it->first;
                if (seen.find(child)!=seen.end()) continue;
                else {
                    if (dist.find(child)!=dist.end()) {
                        new_dist = dist[current] + it->second;
                        old_dist = dist[child];
                        if (new_dist < old_dist) {
                            dist[child] = new_dist;
                            invert_dist[old_dist].erase(child); 
                            invert_dist[new_dist].insert(child); 
                            queue.push(new_dist);
                        }
                    } 
                    // stop if max_dist is reached
                    if (dist[child] >= max_distance) 
                        for (set<pair<int,float>>::iterator it2=edges[child].begin(); it2!=edges[child].end(); it2++)
                            seen.insert(it2->first);
                }
            }
        }

        for (map<int,float>::iterator nodes=dist.begin(); nodes!=dist.end(); nodes++) {
            sum += nodes->second;
        }
      
        return sum;
    }

  
    int current_pos, nbr_of_uedges, nbr_of_uedges_minus_one;
    map<int,set<pair<int,float>>> edges;
    string input_file_name, output_rank;
    fstream input_file;
    float max_distance;
  
};


int main(){
    cout << "--------------------------------- FIRST SIMPLE TEST ----------------------------------\n";
    Graph g = Graph("graph_cpp_.txt");
    g.read();
    g.print();
    cout << "The centrality rank is " << g.centrality(10000000) << "\n";
    return 0;
}
