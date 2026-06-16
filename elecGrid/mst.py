import sys

# Input
data=sys.stdin.read().strip().split()
it=iter(data)
n=int(next(it))
e=int(next(it))

# Build list of edges as tuples (weight, u, v)
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

# Find function
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x

total=0
mst_edges=[]

# Iterate over all edges in ascending weight order
for w, u, v in edges:
    # Find roots of the sets containing u and v
    ru, rv=find(u), find(v)
    # If they are in different sets, add them together
    if ru!=rv:
        # Union by rank: attach smaller rank tree under larger rank tree
        if rank[ru]<rank[rv]:
            parent[ru]=rv
        elif rank[ru]>rank[rv]:
            parent[rv]=ru
        else:
            # If ranks are equal, make one root the parent and increment its rank
            parent[rv]=ru
            rank[ru]+=1
        
        # Update total and edge list
        total+=w
        mst_edges.append((u, v))
        # Stop at n-1 edges
        if len(mst_edges)==n-1:
            break

# Output
sys.stdout.write(total)
sys.stdout.write(n-1)
for u, v in mst_edges:
    sys.stdout.write(u, v)