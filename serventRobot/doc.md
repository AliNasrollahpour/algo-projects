# Full Documentation for Teleporting Robot Customer Visit Problem

## Table of Contents
1. [Overview](#overview)
2. [Input Format](#input-format)
3. [Output Format](#output-format)
4. [Data Structures](#data-structures)
5. [Function Descriptions](#function-descriptions)
6. [Algorithm Explanation](#algorithm-explanation)
7. [Example](#example)
8. [Assumptions and Limitations](#assumptions-and-limitations)

---

## Overview

This program solves a path planning problem on a 2D grid where a robot starts at position `(0,0)` (marked as `S`), has an initial energy budget `l`, and aims to serve as many customers (cells marked `G`) as possible. Movement costs energy (except when staying on `S` or using teleporters). Teleporters (`T`) allow instantaneous jumps to predefined destinations without energy cost. Obstacles (`X`) block movement. The program computes:

- Maximum number of customers that can be served.
- Remaining energy after that optimal path.
- The sequence of grid positions (and teleport indications) that achieves this.

The solution uses a dynamic programming / BFS-like state propagation over grid cells, storing the best state (customers visited, remaining energy) reachable at each cell.

---

## Input Format

The input consists of:

1. **First line**: three integers  
   `n m l`  
   - `n` = number of rows  
   - `m` = number of columns  
   - `l` = initial energy (≥0)

2. **Next n lines**: each contains `m` tokens (space‑separated) representing grid cells.  
   Tokens can be:
   - `S` – start cell (exactly one, at (0,0) assumed)
   - `G` – customer
   - `X` – obstacle
   - `T` – teleporter (may appear multiple times)

3. **Following lines**: teleport definitions, one per `T` in the grid (order arbitrary).  
   Format: `Teleport: (x1,y1) -> (x2,y2)`  
   Means stepping on `(x1,y1)` teleports you to `(x2,y2)`.  
   The input ends after the last teleport definition.  
   There is exactly one teleport definition for each `T` in the grid.

**Important**: The grid cell `(0,0)` must be `S` (start). Teleporters are **directed** – the mapping is from source to destination. A teleporter cell itself can be traversed like a normal cell, but when entered from any direction, the robot is instantly moved to its destination (without consuming energy). The destination cannot be an obstacle.

---

## Output Format

The program prints to standard output:

```
Max customers served: C
Energy used: U
Path:
P1 -> P2 -> ... -> Pk
```

- `C` = maximum number of customers served.
- `U` = total energy consumed (`l` minus remaining energy).
- `Path` = sequence of steps. Positions are printed as `(x,y)`. If a teleport is used, the step is followed by `T` (printed on the same line before the arrow). Example:  
  `(0,0) -> (1,2) -> T -> (5,5)`

If no path exists (even to reach any customer), the program outputs `Max customers served: 0` and `Path: (0,0)`.

---

## Data Structures

### `struct point`
Represents a grid cell.
- `int x, y` – coordinates.
- `string id` – token from input (`S`, `G`, `X`, `T`).
- `state st` – best known state for reaching this cell (see below).

### `struct state`
Stores the best known way to reach a cell.
- `int customersVisited` – number of customers served so far.
- `int remainingEnergy` – energy left after reaching this cell.
- `int sourceX, sourceY` – previous cell coordinates (for path reconstruction).
- `bool sourceTel` – true if the move into this cell was via teleport.

### `result`
Holds the final answer.
- `int customers`
- `int energy` (remaining)
- `string path` – formatted path string.

### Auxiliary maps
- `map<pair<int,int>, pair<int,int>> teleMap` – maps a destination `(x2,y2)` to its teleporter source `(x1,y1)`. This is built from input lines.
- `map<pair<int,int>, vector<pair<int,int>>> teleOut` – reverse mapping (source → list of destinations) for efficient propagation.

---

## Function Descriptions

### `string getPointString(int x, int y)`
Returns a string of the form `"(x,y)"`.

### `bool isInaccessible(state& s)`
Returns true if the state has not been reached yet (both fields equal -1).

### `void setInaccessible(state& s)`
Resets a state to the “unreachable” marker.

### `void setState(state& s, int c, int e, int sx, int sy)`
Sets the state fields (without `sourceTel`). Used for initialization.

### `void copyState(state& dest, state& src, int sx, int sy)`
Copies the customer count and remaining energy from `src` to `dest`, and sets the source coordinates. (Note: `sourceTel` is not copied; it must be set explicitly by the caller.)

### `state* compareStates(state* a, state* b)`
Compares two states. Returns the better one according to:
- higher `customersVisited` wins; if equal,
- higher `remainingEnergy` wins.
Treats inaccessible states as worse than any accessible state.

### `void buildStateTable(vector<vector<point>>& grid, map<pair<int,int>, pair<int,int>>& teleMap, int n, int m)`
Reads the grid and teleport definitions from `std::cin`.  
- Resizes `grid` to `n x m`.
- For each cell, reads its token, stores it, and initialises its `state` as inaccessible.
- Counts teleporters `t`.
- Reads the teleport definitions (exactly `t` lines) and populates `teleMap` with `destination → source`.

### `void propagateStates(vector<vector<point>>& grid, map<pair<int,int>, pair<int,int>>& teleMap, int n, int m, int l)`
Performs a BFS‑like propagation of states starting from `(0,0)`.  
**Steps**:
1. Build `teleOut` (source → list of destinations) from `teleMap`.
2. Initialise `grid[0][0].st` with `customersVisited = 0`, `remainingEnergy = l`, `sourceX = sourceY = -1`.
3. Use a queue of cell coordinates, initially `(0,0)`.
4. While queue not empty:
   - Pop current cell `(i,j)`.
   - If the cell is a teleporter (`id == "T"`), **do not** perform normal moves (robot cannot move normally from a teleporter; it is forced to jump).  
     - Instead, look up `teleOut[(i,j)]` and for each destination `(ni,nj)` that is within bounds and not an obstacle, create a candidate state: same as current, but if destination is `G` increment customers; energy unchanged. If this candidate is better than the existing state at `(ni,nj)`, update and push `(ni,nj)`.
   - If the cell is **not** a teleporter, try moving **down** `(i+1,j)` and **right** `(j+1,m)` (only two directions – note: the original code does **not** consider up/left moves; this assumes movement only down/right, which is typical for a DAG approach).  
     For each valid neighbour that is not an obstacle:
     - Candidate state: copy current.
     - If neighbour is **not** `S`, decrement energy by 1.
     - If energy becomes negative, discard.
     - If neighbour is `G`, increment customers.
     - Compare with existing state on neighbour; if better, update and push neighbour.
5. States are stored with back‑pointers (`sourceX`, `sourceY`, `sourceTel`) for later path reconstruction.

### `result findMaxCustomerPath(vector<vector<point>>& grid, int n, int m)`
Scans all reachable states (non‑inaccessible) to find the one with maximum customers, breaking ties by higher remaining energy.  
Then reconstructs the path by backtracking from that cell:
- Push current coordinates.
- If `sourceTel` is true, push a special marker `"T"`.
- Move to the source cell.
- Stop when reaching a cell with `id == "S"` (or when source coordinates are -1).
- Reverse the collected sequence and format it with ` -> ` separators.

### `int main()`
Orchestrates the whole process:
- Reads `n, m, l`.
- Calls `buildStateTable` and `propagateStates`.
- Calls `findMaxCustomerPath`.
- Prints the result.

---

## Algorithm Explanation

The problem is essentially a resource‑constrained path optimisation on a directed acyclic graph if we restrict moves to down/right (as the code does). However teleports can jump anywhere, potentially creating cycles, but the energy only decreases on normal moves (teleports are free) and customers are only counted when landing on `G`. The algorithm uses dynamic programming where each cell stores the best (customers, energy) pair reachable at that cell.

**Key properties**:
- **Movement**: Only down and right for normal steps (no up/left). This makes the graph acyclic if we ignore teleports. Teleports can go backwards but cannot increase energy.
- **Energy consumption**: Moving onto any cell except `S` costs 1 energy. Teleportation costs 0.
- **State dominance**: State A dominates state B if `A.customers >= B.customers` and `A.energy >= B.energy` (with at least one strict). The algorithm uses a weaker but sufficient comparison: when updating a neighbour, it keeps the state if either customers are higher, or customers equal and energy higher.
- **Propagation order**: A queue ensures that improvements are propagated. Because teleports can create cycles, the algorithm may update a cell multiple times; the queue handles this until convergence (the state space is finite: customers ≤ number of `G`, energy ≤ `l`).

**Teleporter handling**:
- Teleporters are considered “forced” – when you land on a teleporter cell (by any means), you immediately jump to its destination. Therefore normal moves from a teleporter are disabled.
- The teleport itself does not consume energy, but you still count a customer if the destination is `G`.

**Path reconstruction**:
- Every state stores the coordinates of the previous cell and whether the transition was a teleport.
- At the end, the best state is chosen, and we backtrack.

**Complexity**:
- O(n·m·l·(outdegree)) in worst case, but with queue propagation and state pruning it is practical for small grids and moderate energy.

---

## Compilation and Execution

Compile with a C++11 (or later) compiler, e.g.:
```bash
g++ -std=c++11 robot.cpp -o robot
```

Run with input redirection:
```bash
./robot < input.txt
```

The program reads from `std::cin` and writes to `std::cout`.