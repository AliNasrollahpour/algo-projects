import sys

def main():
    # Read first line
    n, e = map(int, input().split())

    # Build list of edges
    edges = []
    for _ in range(e):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))

    # Kruskal's algorithm
    edges.sort()

    # DSU with size n+1
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path compression
            x = parent[x]
        return x

    total = 0
    mst_edges = []

    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            # Union by rank
            if rank[ru] < rank[rv]:
                parent[ru] = rv
            elif rank[ru] > rank[rv]:
                parent[rv] = ru
            else:
                parent[rv] = ru
                rank[ru] += 1

            total += w
            mst_edges.append((u, v))
            if len(mst_edges) == n - 1:
                break

    # Output
    out_lines = [str(total)]
    out_lines.append(f"{len(mst_edges)}")
    for u, v in mst_edges:
        out_lines.append(f"{u} {v}")
    sys.stdout.write("\n".join(out_lines))

    return mst_edges

if __name__ == "__main__":
    main()