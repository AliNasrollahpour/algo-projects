#include <cstddef>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct point{
    int x;
    int y;
    int type; //0=barier, 1=start, 2=guest, 3=teleport pad, 4=empty
    int dx=-1; //destenation of teleport
    int dy=-1; //destenation of teleport
};

struct valuePair{
    int guestsServed=-1; //-1=unassigned
    int energyLeft=-1; //-1unassigned
    point parent=NULL;
};

point input(vector<vector<point> >& map, int& initEnergy){
    int n, m; cin>>n>>m>>initEnergy;
    point start, barier; barier.y=m;
    map.assign(n+1, vector<point>(m+1));
    for(int i=0; i<n; i++){
        for(int j=0; j<m; j++){
            char tmp; cin>>tmp;
            point p;
            p.x=i; p.y=j;
            switch(tmp){
                case 'X':
                    p.type=0;
                    break;
                case 'S':
                    p.type=1;
                    start=p;
                    break;
                case 'G':
                    p.type=2;
                    break;
                case 'T':
                    p.type=3;
                    break;
                default:
                    p.type=4;
            }
            map[i][j]=p;
        }
        barier.x=i;
        map[i][m]=barier;
    }

    for(int j=0; j<m+1; j++){
        barier.y=j;
        map[n][j]=barier;    
    }

    string s;
    while(getline(cin, s)){
        int x, y, dx, dy;
        sscanf(s.c_str(), "Teleport: (%d,%d) -> (%d,%d)", &x, &y, &dx, &dy);
        map[x][y].dx=dx; map[x][y].dy=dy; 
    }
    return start;
}

void DFS(const vector<vector<point> >& map, vector<vector<valuePair> >& valueMap, const point current);

void createNextPoint(const vector<vector<point> >& map, vector<vector<valuePair> >& valueMap, const point current, const point parent){
    //down
    if(map[current.x+1][current.y].type &&
    !(valueMap[current.x+1][current.y].guestsServed>valueMap[current.x][current.y].guestsServed+map[current.x+1][current.y].type==2
    && (valueMap[current.x+1][current.y].guestsServed!=valueMap[current.x][current.y].guestsServed+map[current.x+1][current.y].type==2
        || valueMap[current.x+1][current.y].energyLeft<valueMap[current.x][current.y].energyLeft)
    )){
        valueMap[current.x+1][current.y].parent=parent;
        valueMap[current.x+1][current.y].energyLeft=valueMap[current.x][current.y].energyLeft-1;
        valueMap[current.x+1][current.y].guestsServed=valueMap[current.x][current.y].guestsServed;
        if(map[current.x+1][current.y].type==2) valueMap[current.x+1][current.y].guestsServed++;
        if(map[current.x+1][current.y].type==3){
            point jumpPoint = map[map[current.x+1][current.y].dx][map[current.x+1][current.y].dy];
            createNextPoint(map, valueMap, jumpPoint, map[current.x+1][current.y]);
        }
        point nextPoint=map[current.x+1][current.y];
        DFS(map, valueMap, nextPoint);
    }
    //right
    if(map[current.x+1][current.y].type &&
    !(valueMap[current.x][current.y+1].guestsServed>valueMap[current.x][current.y].guestsServed+map[current.x][current.y+1].type==2
    && (valueMap[current.x][current.y+1].guestsServed!=valueMap[current.x][current.y].guestsServed+map[current.x][current.y+1].type==2
        || valueMap[current.x][current.y+1].energyLeft<valueMap[current.x][current.y].energyLeft)
    )){
        valueMap[current.x][current.y+1].parent=parent;
        valueMap[current.x][current.y+1].energyLeft=valueMap[current.x][current.y].energyLeft-1;
        valueMap[current.x][current.y+1].guestsServed=valueMap[current.x][current.y].guestsServed;
        if(map[current.x][current.y+1].type==2) valueMap[current.x][current.y+1].guestsServed++;
        if(map[current.x][current.y+1].type==3){
            point jumpPoint = map[map[current.x][current.y+1].dx][map[current.x][current.y+1].dy];
            createNextPoint(map, valueMap, jumpPoint, map[current.x][current.y+1]);
        }
        point nextPoint=map[current.x][current.y+1];
        DFS(map, valueMap, nextPoint);
    }
}

void DFS(const vector<vector<point> >& map, vector<vector<valuePair> >& valueMap, const point current){
    if(valueMap[current.x][current.y].energyLeft) createNextPoint(map, valueMap, current, current);
}

point findBest(const vector<vector<point> >& map, const vector<vector<valuePair> > valueMap){
    int bx=0, by=0;
    for(int i=0; i<map.size(); i++)
        for(int j=0; j<map[i].size(); j++)
            if(valueMap[i][j].guestsServed>=valueMap[bx][by].guestsServed && valueMap[i][j].energyLeft>valueMap[bx][by].energyLeft){
                bx=i; by=j;
            }
    return map[bx][by];
}

vector<point> path(const vector<vector<point> >& map, const vector<vector<valuePair> >& valueMap){
    vector<point> path;
    path.push_back(findBest(map, valueMap));
    while(valueMap[path.back().dx][path.back().dx].parent)
        path.push_back(valueMap[path.back().dx][path.back().dx].parent);
    return path;
}

void print(){
    //--
}

int main(){
    vector<vector<point> > map;
    int initEnergy;
    point start=input(map, initEnergy);

    vector<vector<valuePair> > valueMap(map.size(), vector<valuePair>(map[0].size()));
    DFS(map, valueMap, start);

    //--
}