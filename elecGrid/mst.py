import sys

# input
data=sys.stdin.read().strip().split()
if not data:
    return
it=iter(data)
n=int(next(it))
e=int(next(it))

edges=[]
for _ in range(e):
    u=int(next(it))
    v=int(next(it))
    w=int(next(it))
    edges.append((w, u, v))

# Logic

# Output
print(total)
print(n-1)
for u, v in mst_edges:
    print(u, v)
