import sys

class DSU:
    def __init__(self, n):
        self.parent=list(range(n))
        self.rank=[0]*n

    def find(self, x):
        # Iterative path compression
        while self.parent[x]!=x:
            self.parent[x]=self.parent[self.parent[x]]
            x=self.parent[x]
        return x

    def union(self, x, y):
        rx=self.find(x)
        ry=self.find(y)
        if rx==ry:
            return
        # Union by rank
        if self.rank[rx]<self.rank[ry]:
            self.parent[rx]=ry
        elif self.rank[rx]>self.rank[ry]:
            self.parent[ry]=rx
        else:
            self.parent[ry]=rx
            self.rank[rx]+=1

# Input
def parse_input():
    # Read all tokens (whitespace-separated)
    tokens=sys.stdin.read().strip().split()
    if not tokens:
        return None

    it=iter(tokens)

    n=int(next(it))
    e=int(next(it))

    edges=[]
    for _ in range(e):
        u=int(next(it))
        v=int(next(it))
        w=int(next(it))
        m=int(next(it))
        edges.append((u, v, w, m))

    h=int(next(it))
    unharmed=[]
    for _ in range(h):
        u=int(next(it))
        v=int(next(it))
        unharmed.append((u, v))

    B=int(next(it))

    return {
        'n': n,
        'e': e,
        'edges': edges,
        'h': h,
        'unharmed': unharmed,
        'B': B
    }

# Output
def print_output(possible, construction_cost=None, maintenance_cost=None, tree=None):
    if not possible:
        sys.stdout.write("NO\n")
    else:
        out_lines=[]
        sys.stdout.write(construction_cost)
        sys.stdout.write(maintenance_cost)
        sys.stdout.write(len(tree))
        sys.stdout.write("\n".join(f"{u} {v}" for u, v in tree))

# Connecting all the unhramed edges and creating a new graph that only has buildable edges
def preprocess(n, unharmed, edges):
    dsu=DSU(n)

    # Union all unharmed
    for u, v in unharmed:
        dsu.union(u, v)

    # Map each DSU root to a component ID
    RTI={}
    reducedNodes=[]
    for v in range(n):
        root=dsu.find(v)
        if root not in RTI:
            RTI[root]=len(reducedNodes)
            reducedNodes.append(root)
    
    # Build reduced edge list
    reduced=[]
    for u, v, c, m in edges:
        ru=dsu.find(u)
        rv=dsu.find(v)
        if ru!=rv:
            cu=RTI[ru]
            cv=RTI[rv]
            reduced.append((cu, cv, c, m))

    return reducedNodes, reduced

