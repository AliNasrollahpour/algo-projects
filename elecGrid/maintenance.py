import sys
import heapq
from copy import deepcopy
from typing import List, Tuple, Optional

class Edge:
    #Represents an edge with its costs and whether it is a new cable.
    def __init__(self, u: int, v: int, build_cost: float, maint_cost: float, is_new: bool):
        self.u = u
        self.v = v
        self.build_cost = build_cost
        self.maint_cost = maint_cost
        self.is_new = is_new

class DSU:
    #Disjoint Set Union
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

class Node:
    #Branch and Bound search node.
    def __init__(self, level: int, edge_state: List[int], build_cost: float,
                 maint_cost: float, selected_edges: List[int]):
        self.level = level
        self.edge_state = edge_state # -1 excluded, 0 undecided, 1 included
        self.build_cost = build_cost
        self.maint_cost = maint_cost
        self.lower_bound = 0.0
        self.selected_edges = selected_edges

    def __lt__(self, other):
        return self.lower_bound < other.lower_bound

#Global Variables
n = 0
total_edges = 0
budget = 0.0
edges: List[Edge] = []
best_cost = float('inf')
best_maint = float('inf')
best_solution: Optional[List[int]] = None

def calculate_lower_bound(node: Node) -> float:
    dsu = DSU(n)
    bound = node.build_cost

    # Include mandatory edges
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            if not dsu.union(edges[i].u, edges[i].v):
                return float('inf')   # cycle among forced edges

    # Greedily complete the tree
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            continue
        if node.edge_state[i] == -1:
            continue
        # undecided edge
        if dsu.union(edges[i].u, edges[i].v):
            bound += edges[i].build_cost   # unharmed edges add 0

    if not dsu.connected():
        return float('inf')

    return bound


def feasible(node: Node) -> bool:
    # Budget constraint
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

    # Check connectivity possibility with remaining edges
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


def is_complete(node: Node) -> bool:
    return sum(1 for s in node.edge_state if s == 1) == n - 1


def is_valid_spanning_tree(node: Node) -> bool:
    dsu = DSU(n)
    for i in range(total_edges):
        if node.edge_state[i] == 1:
            if not dsu.union(edges[i].u, edges[i].v):
                return False
    return dsu.connected()


def copy_node(node: Node) -> Node:
    new_node = Node(
        level=node.level,
        edge_state=copy.deepcopy(node.edge_state),
        build_cost=node.build_cost,
        maint_cost=node.maint_cost,
        selected_edges=copy.deepcopy(node.selected_edges),
    )
    new_node.lower_bound = node.lower_bound
    return new_node


def solve_cmst() -> None:
    global best_cost, best_maint, best_solution

    # Sort all edges by build cost
    edges.sort(key=lambda edge: edge.build_cost)

    # Priority queue: (lower_bound, tie_breaker, node)
    pq: List[Tuple[float, int, Node]] = []
    counter = 0

    root = Node(
        level=-1,
        edge_state=[0] * total_edges,
        build_cost=0.0,
        maint_cost=0.0,
        selected_edges=[],
    )
    root.lower_bound = calculate_lower_bound(root)

    heapq.heappush(pq, (root.lower_bound, counter, root))
    counter += 1

    while pq:
        _, _, current = heapq.heappop(pq)

        # Bounding
        if current.lower_bound >= best_cost or current.maint_cost > budget:
            continue

        # check for complete solution
        if is_complete(current):
            if is_valid_spanning_tree(current):
                best_cost = current.build_cost
                best_maint = current.maint_cost
                best_solution = current.selected_edges
            continue

        # No more edges to decide
        if current.level == total_edges - 1:
            continue

        next_edge = current.level + 1

        #Left child : include next edge
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
            if left.lower_bound < best_cost:
                heapq.heappush(pq, (left.lower_bound, counter, left))
                counter += 1

        #Right child : exclude next edge
        right = copy_node(current)
        right.level = next_edge
        right.edge_state[next_edge] = -1

        if feasible(right):
            right.lower_bound = calculate_lower_bound(right)
            if right.lower_bound < best_cost:
                heapq.heappush(pq, (right.lower_bound, counter, right))
                counter += 1

if __name__ == "__main__":
    data = sys.stdin.read().strip().split()
    it = iter(data)

    n = int(next(it))
    e_original = int(next(it))

    # Read e new edges
    edges = []
    for _ in range(e_original):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = float(next(it))
        m = float(next(it))
        edges.append(Edge(u, v, w, m, is_new=True))

    h = int(next(it))
    for _ in range(h):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        # Unharmed: build cost = 0
        edges.append(Edge(u, v, 0.0, 0.0, is_new=False))

    budget = float(next(it))

    total_edges = len(edges)

    solve_cmst()

    if best_solution is None:
        print("NO")
    else:
        print(f"{best_cost}")
        print(f"{best_maint}")
        print(f"{n - 1}")
        for idx in best_solution:
            edge = edges[idx]
            # Print only endpoints (1‑based), no costs
            print(f"{edge.u + 1} {edge.v + 1}")