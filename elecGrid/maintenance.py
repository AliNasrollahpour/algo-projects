import sys

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
    built_edges=[]
    for _ in range(h):
        u=int(next(it))
        v=int(next(it))
        built_edges.append((u, v))

    B=int(next(it))

    return {
        'n': n,
        'e': e,
        'edges': edges,
        'h': h,
        'built_edges': built_edges,
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