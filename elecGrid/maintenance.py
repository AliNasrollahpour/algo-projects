import sys
import heapq
from typing import List, Tuple, Optional

INF = 10**1000

# Edge representation: stores both endpoints, build cost, maintenance cost, and whether it is a new road.
class Edge:
    def __init__(self, u: int, v: int, build_cost: int, maint_cost: int, is_new: bool):
        self.u = u
        self.v = v
        self.build_cost = build_cost
        self.maint_cost = maint_cost
        self.is_new = is_new

# Disjoint Set Union (DSU) structure for cycle detection and connectivity checks.
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        self.components -= 1
        return True

    def connected(self) -> bool:
        return self.components == 1

# Node in the branch-and-bound search tree. Each node represents a partial assignment of edge states.
class Node:
    def __init__(self, level: int, edge_state: List[int], build_cost: int,
                 maint_cost: int, selected_edges: List[int]):
        self.level = level
        self.edge_state = edge_state      # -1 excluded, 0 undecided, 1 included
        self.build_cost = build_cost
        self.maint_cost = maint_cost
        self.lower_bound = 0
        self.selected_edges = selected_edges

    def __lt__(self, other):
        return self.lower_bound < other.lower_bound

# Global variables
n = 0
total_edges = 0
budget = 0
edges: List[Edge] = []
best_cost = INF
best_maint = INF
best_solution: Optional[List[int]] = None

# A lower bound on the total build cost for a partial solution.
# The bound was obtained by forcing already‑included edges, then greedily adding the cheapest available undecided edges
# until the graph becomes connected. If a cycle is formed among forced edges, INF is returned.
def calculate_lower_bound(node: Node) -> int:
    dsu = DSU(n)
    bound = node.build_cost

    # Include mandatory edges
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            if not dsu.union(edges[i].u, edges[i].v):
                return INF   # cycle among forced edges

    # Greedily complete the tree using undecided edges
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            continue
        if node.edge_state[i] == -1:
            continue
        if dsu.union(edges[i].u, edges[i].v):
            bound += edges[i].build_cost

    if not dsu.connected():
        return INF
    return bound

# Feasibility checks for the current partial assignment
def feasible(node: Node) -> bool:
    if node.maint_cost > budget:
        return False

    included = sum(1 for s in node.edge_state if s == 1)
    undecided = sum(1 for s in node.edge_state if s == 0)

    if included > n - 1:
        return False

    needed = (n - 1) - included
    if undecided < needed:
        return False

    # Cycle check among included edges
    dsu = DSU(n)
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            if not dsu.union(edges[i].u, edges[i].v):
                return False

    # Connectivity possibility
    components = dsu.components
    possible_connections = 0
    for i in range(total_edges):
        if node.edge_state[i] == 0:
            u, v = edges[i].u, edges[i].v
            if dsu.find(u) != dsu.find(v):
                possible_connections += 1

    if possible_connections < components - 1:
        return False
    return True

# A node is complete when exactly n‑1 edges have been selected.
def is_complete(node: Node) -> bool:
    return sum(1 for s in node.edge_state if s == 1) == n - 1

# Verifies that the selected edges form a spanning tree (i.e., connected and acyclic).
def is_valid_spanning_tree(node: Node) -> bool:
    dsu = DSU(n)
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            if not dsu.union(edges[i].u, edges[i].v):
                return False
    return dsu.connected()

# A shallow copy of a node was created to allow independent exploration of its children.
def copy_node(node: Node) -> Node:
    new_node = Node(
        level=node.level,
        edge_state=node.edge_state.copy(),
        build_cost=node.build_cost,
        maint_cost=node.maint_cost,
        selected_edges=node.selected_edges.copy(),
    )
    new_node.lower_bound = node.lower_bound
    return new_node

# Main branch‑and‑bound search for the constrained minimum spanning tree problem.
# Edges are considered in increasing order of build cost; the search branches on inclusion/exclusion.
def solve_cmst() -> None:
    global best_cost, best_maint, best_solution

    edges.sort(key=lambda edge: edge.build_cost)

    pq: List[Tuple[int, int, Node]] = []
    counter = 0

    root = Node(
        level=-1,
        edge_state=[0] * total_edges,
        build_cost=0,
        maint_cost=0,
        selected_edges=[],
    )
    root.lower_bound = calculate_lower_bound(root)
    heapq.heappush(pq, (root.lower_bound, counter, root))
    counter += 1

    while pq:
        _, _, current = heapq.heappop(pq)
        # Prune if the lower bound already exceeds the best known build cost,
        # or if maintenance cost already exceeds the budget.
        if current.lower_bound > best_cost or current.maint_cost > budget:
            continue

        if is_complete(current) and is_valid_spanning_tree(current):
            if (current.build_cost < best_cost or
                (current.build_cost == best_cost and current.maint_cost < best_maint)):
                best_cost = current.build_cost
                best_maint = current.maint_cost
                best_solution = current.selected_edges.copy()
            continue

        if current.level == total_edges - 1:
            continue

        next_edge = current.level + 1

        # Left child: include the next edge
        left = copy_node(current)
        left.level = next_edge
        left.edge_state[next_edge] = 1
        left.selected_edges.append(next_edge)

        edge = edges[next_edge]
        left.build_cost += edge.build_cost
        if edge.is_new:
            left.maint_cost += edge.maint_cost

        if feasible(left):
            left.lower_bound = calculate_lower_bound(left)
            heapq.heappush(pq, (left.lower_bound, counter, left))
            counter += 1

        # Right child: exclude the next edge
        right = copy_node(current)
        right.level = next_edge
        right.edge_state[next_edge] = -1

        if feasible(right):
            right.lower_bound = calculate_lower_bound(right)
            heapq.heappush(pq, (right.lower_bound, counter, right))
            counter += 1

if __name__ == "__main__":
    n, e_original = map(int, input().split())

    edges = []
    for _ in range(e_original):
        u, v, w, m = input().split()
        u = int(u) - 1
        v = int(v) - 1
        w = int(w)
        m = int(m)
        edges.append(Edge(u, v, w, m, is_new=True))

    h = int(input())
    for _ in range(h):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append(Edge(u, v, 0, 0, is_new=False))

    budget = int(input())
    total_edges = len(edges)

    solve_cmst()

    print()
    if best_solution is None:
        print("NO")
    else:
        print(f"{best_cost}")
        print(f"{best_maint}")
        print(f"{n - 1}")
        for idx in best_solution:
            edge = edges[idx]
            print(f"{edge.u + 1} {edge.v + 1}")