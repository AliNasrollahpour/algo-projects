import sys

# input
data=sys.stdin.read().strip().split()
it=iter(data)
n=int(next(it))
e=int(next(it))

edges=[]
for _ in range(e):
    u=int(next(it))
    v=int(next(it))
    w=int(next(it))
    edges.append((w, u, v))

# Logic (Kruskal)
edges.sort()
parent=list(range(n))
rank=[0]*n

def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x

total=0
mst_edges=[]
for w, u, v in edges:
    ru, rv=find(u), find(v)
    if ru!=rv:
        if rank[ru]<rank[rv]:
            parent[ru]=rv
        elif rank[ru]>rank[rv]:
            parent[rv]=ru
        else:
            parent[rv]=ru
            rank[ru]+=1
        
        total+=w
        mst_edges.append((u, v))
        if len(mst_edges)==n-1:
            break

# Output
sys.stdout.write(total)
sys.stdout.write(n-1)
for u, v in mst_edges:
    sys.stdout.write(u, v)
