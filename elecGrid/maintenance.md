## Documentation

### Overview

This program solves the **Constrained Minimum Spanning Tree (CMST)** problem using a **Branch-and-Bound** algorithm. The objective is to find a spanning tree with the **minimum total construction cost** while ensuring that the **maintenance cost of newly built roads does not exceed a given budget**.

---

### Main Components

* **Edge**

  * Represents a road in the graph.
  * Stores its endpoints, construction cost, maintenance cost, and whether it is an existing or newly built road.

* **DSU (Disjoint Set Union)**

  * Maintains connected components efficiently.
  * Used for cycle detection and connectivity checks.

* **Node**

  * Represents a partial solution in the Branch-and-Bound search tree.
  * Stores the current edge decisions (included, excluded, undecided), accumulated costs, and selected edges.

---

### Algorithm

1. Sort all edges by **construction cost**.
2. Start from an empty solution (the root node).
3. Repeatedly expand the node with the **smallest lower bound** using a priority queue.
4. For each edge, create two branches:

   * **Include** the edge.
   * **Exclude** the edge.
5. Before expanding a branch, perform feasibility checks:

   * Maintenance cost does not exceed the budget.
   * No cycles are formed.
   * A spanning tree is still possible.
6. Compute a **lower bound** on the minimum possible construction cost by greedily completing the partial solution.
7. Prune branches whose lower bound is already worse than the best solution found.
8. When a complete valid spanning tree is reached, update the best solution if it has a lower construction cost (or lower maintenance cost in case of a tie).

---

### Time Complexity

The Branch-and-Bound algorithm has an **exponential worst-case time complexity**, since every edge may be either included or excluded:

$$
O(2^E)
$$

where $E$ is the number of edges.

However, the use of:

* feasibility checks,
* lower-bound estimation, and
* priority-queue exploration

significantly reduces the search space in practice by pruning many branches before they are fully explored.

---

### Input

* Number of vertices and candidate new roads.
* Information for each new road:

  * endpoints,
  * construction cost,
  * maintenance cost.
* Number of existing roads.
* Endpoints of each existing road.
* Maximum allowed maintenance budget.

---

### Output

If no feasible spanning tree exists, the program prints:

```
NO
```

Otherwise, it prints:

1. Minimum construction cost.
2. Total maintenance cost.
3. Number of edges in the spanning tree.
4. The list of selected edges.
