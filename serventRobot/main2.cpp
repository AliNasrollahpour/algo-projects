
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

string getPointString(int x, int y){
    return "("+to_string(x)+","+to_string(y)+")";
}

struct state{
    int customersVisited;
    int remainingEnergy;
    int sourceX;
    int sourceY;
    bool sourceTel;

    state(){
        customersVisited=-1;
        remainingEnergy=-1;
        sourceX=-1;
        sourceY=-1;
        sourceTel=false;
    }
};

struct point{
    int x;
    int y;
    string id;
    state st;
};

bool isInaccessible(state& s){
    return(s.customersVisited==-1 && s.remainingEnergy==-1);
}

void setInaccessible(state& s){
    s.customersVisited=-1;
    s.remainingEnergy=-1;
    s.sourceX=-1;
    s.sourceY=-1;
    s.sourceTel=false;
}

void setState(state& s, int c, int e, int sx, int sy){
    s.customersVisited=c;
    s.remainingEnergy=e;
    s.sourceX=sx;
    s.sourceY=sy;
    s.sourceTel=false;
}

void copyState(state& dest, state& src, int sx, int sy){
    dest.customersVisited=src.customersVisited;
    dest.remainingEnergy=src.remainingEnergy;
    dest.sourceX=sx;
    dest.sourceY=sy;
    // sourceTel is not copied; it depends on transition logic
}

state* compareStates(state* a, state* b){
    if(isInaccessible(*b)) return a;
    if(isInaccessible(*a)) return b;
    if(a->customersVisited>b->customersVisited) return a;
    if(a->customersVisited==b->customersVisited && a->remainingEnergy>b->remainingEnergy) return a;
    return b;
}

void buildStateTable(vector<vector<point> >& grid, map<pair<int,int>, pair<int,int> >& teleMap, int n, int m){
    grid.resize(n, vector<point>(m));
    int t=0;
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            string token;
            cin>>token;
            grid[i][j].x=i;
            grid[i][j].y=j;
            grid[i][j].id=token;
            setInaccessible(grid[i][j].st);   // initially all inaccessible
            if(token=="T") t++;
        }
    }
    string buffer;
    getline(cin, buffer);   // clear rest of line
    getline(cin, buffer);   // empty line before teleport definitions
    string line;
    while(t--){
        getline(cin, line);
        if(line.empty()) continue;
        int x1, y1, x2, y2;
        if(sscanf(line.c_str(), "Teleport:(%d,%d) -> (%d,%d)", &x1, &y1, &x2, &y2)==4)
            teleMap[make_pair(x2, y2)]=make_pair(x1, y1);
    }
}

void propagateStates(vector<vector<point> >& grid, map<pair<int,int>, pair<int,int> >& teleMap, int n, int m, int l){
    // Build reverse teleport map: source -> list of destinations
    map<pair<int,int>, vector<pair<int,int> > > teleOut;
    map<pair<int,int>, pair<int,int> >::iterator it;
    for(it=teleMap.begin(); it!=teleMap.end(); it++){
        pair<int,int> dest=it->first;
        pair<int,int> src=it->second;
        teleOut[src].push_back(dest);
    }

    // Initialize start cell(0,0)
    grid[0][0].st.customersVisited=0;
    grid[0][0].st.remainingEnergy=l;
    grid[0][0].st.sourceX=-1;
    grid[0][0].st.sourceY=-1;
    grid[0][0].st.sourceTel=false;

    queue<pair<int,int> >q;
    q.push(make_pair(0,0));

    while(!q.empty()){
        pair<int,int> cur=q.front();
        q.pop();
        int i=cur.first;
        int j=cur.second;
        state& curState=grid[i][j].st;
        if(isInaccessible(curState)) continue;   // safety

        // Normal moves
        if(grid[i][j].id!="T"){
            // Move down
            if(i+1<n){
                int ni=i+1, nj=j;
                if(grid[ni][nj].id!="X"){
                    state cand=curState;
                    if(grid[ni][nj].id!="S") cand.remainingEnergy--;
                    if(cand.remainingEnergy >= 0){
                        if(grid[ni][nj].id=="G") cand.customersVisited++;
                        state& existing=grid[ni][nj].st;
                        if(isInaccessible(existing) || cand.customersVisited>existing.customersVisited ||
                           (cand.customersVisited==existing.customersVisited && cand.remainingEnergy>existing.remainingEnergy)
                        ){
                            existing=cand;
                            existing.sourceX=i;
                            existing.sourceY=j;
                            existing.sourceTel=false;
                            q.push(make_pair(ni, nj));
                        }
                    }
                }
            }
            // Move right
            if(j+1<m){
                int ni=i, nj=j+1;
                if(grid[ni][nj].id!="X"){
                    state cand=curState;
                    if(grid[ni][nj].id!="S") cand.remainingEnergy--;
                    if(cand.remainingEnergy >= 0){
                        if(grid[ni][nj].id=="G") cand.customersVisited++;
                        state& existing=grid[ni][nj].st;
                        if(isInaccessible(existing) || cand.customersVisited>existing.customersVisited ||
                           (cand.customersVisited==existing.customersVisited && cand.remainingEnergy>existing.remainingEnergy)
                        ){
                            existing=cand;
                            existing.sourceX=i;
                            existing.sourceY=j;
                            existing.sourceTel=false;
                            q.push(make_pair(ni, nj));
                        }
                    }
                }
            }
        }

        // Teleport moves
        if(teleOut.count(make_pair(i,j))>0){
            vector<pair<int,int> >& dests=teleOut[make_pair(i,j)];
            for(size_t k=0; k<dests.size(); ++k){
                int ni=dests[k].first;
                int nj=dests[k].second;
                if(ni >= 0 && ni<n && nj >= 0 && nj<m && grid[ni][nj].id!="X"){
                    state cand=curState;   // teleport does not consume energy
                    if(grid[ni][nj].id=="G") cand.customersVisited++;
                    state& existing=grid[ni][nj].st;
                    if(isInaccessible(existing) || cand.customersVisited>existing.customersVisited ||
                       (cand.customersVisited==existing.customersVisited && cand.remainingEnergy>existing.remainingEnergy)
                    ){
                        existing=cand;
                        existing.sourceX=i;
                        existing.sourceY=j;
                        existing.sourceTel=true;
                        q.push(make_pair(ni, nj));
                    }
                }
            }
        }
    }
}

struct result{
    int customers;
    int energy;
    string path;
};

result findMaxCustomerPath(vector<vector<point> >& grid, int n, int m){
    result ans;
    ans.customers=0;
    ans.energy=0;
    ans.path="(0,0)";

    int maxC=-1;
    int maxE=-1;
    int endX=0, endY=0;

    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            if(isInaccessible(grid[i][j].st)) continue;
            if(grid[i][j].st.customersVisited>maxC || (grid[i][j].st.customersVisited==maxC && grid[i][j].st.remainingEnergy>maxE)){
                maxC=grid[i][j].st.customersVisited;
                maxE=grid[i][j].st.remainingEnergy;
                endX=i; endY=j;
            }
        }
    }

    if(maxC==-1) return ans;   // no path found

    ans.customers=maxC;
    ans.energy=maxE;

    // Backtracking
    vector<string> pathVec;
    int curX=endX, curY=endY;
    while(true){
        pathVec.push_back(getPointString(curX, curY));
        if(grid[curX][curY].id=="S") break;

        if(grid[curX][curY].st.sourceTel) pathVec.push_back("T");

        int nextX=grid[curX][curY].st.sourceX;
        int nextY=grid[curX][curY].st.sourceY;
        if(nextX==-1 && nextY==-1) break;   // just in case

        curX=nextX;
        curY=nextY;
    }

    reverse(pathVec.begin(), pathVec.end());
    stringstream ss;
    for(size_t i=0; i<pathVec.size(); i++){
        ss<<pathVec[i];
        if(i!=pathVec.size()-1) ss<<" -> ";
    }
    ans.path=ss.str();

    return ans;
}

int main(){
    int n, m, l;
    cin>>n>>m>>l;

    vector<vector<point> >grid;
    map<pair<int,int>, pair<int,int> >teleMap;

    buildStateTable(grid, teleMap, n, m);
    propagateStates(grid, teleMap, n, m, l);

    result ans=findMaxCustomerPath(grid, n, m);
    cout<<"\nMax customers served: "<<ans.customers<<"\n"
        <<"Energy used: "<<l-ans.energy<<"\n"
        <<"Path:\n"<<ans.path<<endl;

    return 0;
}