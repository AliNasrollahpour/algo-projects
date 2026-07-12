Kruskal's Minimum Spanning Tree (MST) Algorithm
================================================

Purpose
-------
Reads an undirected weighted graph from standard input and computes its
Minimum Spanning Tree using Kruskal's algorithm with Union-Find (DSU)
and path compression + union by rank.

Input Format
------------
First line: two integers `n` and `e` (number of vertices and edges).
Next `e` lines: each contains three integers `u v w` representing an
undirected edge between vertices `u` and `v` with weight `w`.

- Vertices are assumed to be 1‑indexed (labels from 1 to n).
- The graph may be disconnected; the algorithm will output the MST of
  the connected components it can reach (break early after n-1 edges).

Output Format
-------------
If the graph is connected, the output consists of:
- Line 1: total weight of the MST (integer)
- Line 2: number of edges in the MST (which will be n-1)
- Next `n-1` lines: each contains two integers `u v` representing an
  edge included in the MST (order is not guaranteed).

If the graph is disconnected, the MST will have fewer than n-1 edges;
the output still shows the total weight and edge count for the forest.

Algorithm & Complexity
----------------------
- Sorts all edges by weight: O(e log e).
- Processes edges in ascending order, adding an edge if it connects
  two different components (no cycle).
- Uses path compression and union by rank for near‑constant amortized
  time per find/union operation: O(α(n)) per operation.
- Overall time complexity: O(e log e + e α(n)).
- Memory: O(n + e).

Example
-------
Input:
4 5
1 2 10
2 3 15
1 3 5
2 4 20
3 4 25

Output:
35
3
1 3
1 2
2 4