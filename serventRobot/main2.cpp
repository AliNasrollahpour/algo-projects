
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

