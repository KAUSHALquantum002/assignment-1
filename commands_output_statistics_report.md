# CSE 537 - Assignment 1: Execution Statistics, Terminal Outputs, and Critical Analysis

This document compiles the exact commands executed, raw console outputs, performance statistics, and in-depth observations/critical analysis for Questions 1 through 7 of **Project 01: The Searchin' Pac-Man**.

---

## Master Performance Summary Table

| Q# | Search Strategy | Layout / Problem | Heuristic / Cost Function | Solution Cost | Nodes Expanded | Time (s) | Score | Result |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Q1** | DFS | `tinyMaze` | Uniform ($1$) | 10 | 15 | 0.0 | 500.0 | Win |
| **Q1** | DFS | `mediumMaze` | Uniform ($1$) | 130 | 146 | 0.0 | 380.0 | Win |
| **Q1** | DFS | `bigMaze` | Uniform ($1$) | 210 | 390 | 0.0 | 300.0 | Win |
| **Q2** | BFS | `mediumMaze` | Uniform ($1$) | **68** | 269 | 0.0 | 442.0 | Win |
| **Q2** | BFS | `bigMaze` | Uniform ($1$) | **210** | 620 | 0.0 | 300.0 | Win |
| **Q2** | BFS | `eightpuzzle.py` | Uniform ($1$) | 1 | N/A | 0.0 | N/A | Win |
| **Q3** | UCS | `mediumMaze` | `SearchAgent` (Uniform) | **68** | 269 | 0.0 | 442.0 | Win |
| **Q3** | UCS | `mediumDottedMaze` | `StayEastSearchAgent` ($2^x$) | **1** | 186 | 0.0 | 646.0 | Win |
| **Q3** | UCS | `mediumScaryMaze` | `StayWestSearchAgent` ($2^x$) | **68,719,479,864** | 108 | 0.0 | 418.0 | Win |
| **Q4** | A* | `bigMaze` | `manhattanHeuristic` | **210** | **549** | 0.0 | 300.0 | Win |
| **Q4** | DFS | `openMaze` | Uniform ($1$) | 298 | 576 | 0.0 | 212.0 | Win |
| **Q4** | BFS | `openMaze` | Uniform ($1$) | **54** | 682 | 0.0 | 456.0 | Win |
| **Q4** | UCS | `openMaze` | Uniform ($1$) | **54** | 682 | 0.0 | 456.0 | Win |
| **Q4** | A* | `openMaze` | `manhattanHeuristic` | **54** | **535** | 0.0 | 456.0 | Win |
| **Q5** | BFS | `tinyCorners` | `CornersProblem` | **28** | 252 | 0.0 | 512.0 | Win |
| **Q5** | BFS | `mediumCorners` | `CornersProblem` | **106** | 1,966 | 0.0 | 434.0 | Win |
| **Q6** | A* | `mediumCorners` | `cornersHeuristic` | **106** | **741** | 0.0 | 434.0 | Win |
| **Q7** | A* | `testSearch` | `foodHeuristic` | **7** | 10 | 0.0 | 513.0 | Win |
| **Q7** | A* | `trickySearch` | `foodHeuristic` | **60** | **4,137** | 0.3 | 570.0 | Win |

---

## Question 1: Depth-First Search (DFS)

### 1.1 Commands Executed
```bash
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
```

### 1.2 Console Output & Statistics
```text
[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 10 in 0.0 seconds
Search nodes expanded: 15
Pacman emerges victorious! Score: 500

[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 130 in 0.0 seconds
Search nodes expanded: 146
Pacman emerges victorious! Score: 380

[SearchAgent] using function depthFirstSearch
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 210 in 0.0 seconds
Search nodes expanded: 390
Pacman emerges victorious! Score: 300
```

### 1.3 Observations & Critical Analysis
- **Exploration Order**: DFS explores as deep as possible along each branch before backtracking. Because a `Stack` (LIFO) is used, successors are popped in reverse order of insertion. Pushing successors in order `[North, South, East, West]` causes `West` to be popped and explored first.
- **Physical Traversal vs. Search Nodes**: Pac-Man does **not** visit all expanded red squares on its way to the goal. The red squares represent search space exploration; Pac-Man physically travels only along the final returned path.
- **Optimality**: DFS does **not** find a least-cost (optimal) solution. On `mediumMaze`, DFS returns a path of cost **130** (expanding 146 nodes), whereas the optimal path length is **68**.

---

## Question 2: Breadth-First Search (BFS)

### 2.1 Commands Executed
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
python eightpuzzle.py
```

### 2.2 Console Output & Statistics
```text
[SearchAgent] using function bfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 269
Pacman emerges victorious! Score: 442

[SearchAgent] using function bfs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 210 in 0.0 seconds
Search nodes expanded: 620
Pacman emerges victorious! Score: 300

BFS found a path of 1 moves: ['up']
```

### 2.3 Observations & Critical Analysis
- **Optimality**: BFS is guaranteed to find the least-cost (optimal) solution on graphs where all edge step costs are equal ($c=1$). 
- **Comparison to DFS**: On `mediumMaze`, BFS finds the optimal path of length **68** (compared to **130** for DFS), although it expands **269** nodes (compared to 146 for DFS) because it expands nodes in concentric waves (level-by-level).
- **Generic Search Compatibility**: The identical BFS implementation solves the 8-puzzle problem (`eightpuzzle.py`) without code modification.

---

## Question 3: Uniform-Cost Search (UCS)

### 3.1 Commands Executed
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```

### 3.2 Console Output & Statistics
```text
[SearchAgent] using function ucs
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 68 in 0.0 seconds
Search nodes expanded: 269
Pacman emerges victorious! Score: 442

Path found with total cost of 1 in 0.0 seconds
Search nodes expanded: 186
Pacman emerges victorious! Score: 646

Path found with total cost of 68719479864 in 0.0 seconds
Search nodes expanded: 108
Pacman emerges victorious! Score: 418
```

### 3.3 Observations & Critical Analysis
- **Uniform Edge Costs**: On `mediumMaze` with uniform costs ($c=1$), UCS behaves identically to BFS, expanding **269** nodes and returning path cost **68**.
- **`StayEastSearchAgent` on `mediumDottedMaze`**: Exponentially low step costs ($2^x$) assigned to eastern states encourage Pac-Man to move east, yielding a path cost of **1** after expanding **186** nodes.
- **`StayWestSearchAgent` on `mediumScaryMaze`**: Exponentially high step costs ($2^x$) assigned to eastern states steer Pac-Man west to avoid expensive steps, yielding a total cost of **68,719,479,864** after expanding **108** nodes.

---

## Question 4: A* Search

### 4.1 Commands Executed
```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
python pacman.py -l openMaze -p SearchAgent -a fn=dfs
python pacman.py -l openMaze -p SearchAgent -a fn=bfs
python pacman.py -l openMaze -p SearchAgent -a fn=ucs
python pacman.py -l openMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

### 4.2 Console Output & Statistics
```text
[SearchAgent] using function astar and heuristic manhattanHeuristic
[SearchAgent] using problem type PositionSearchProblem
Path found with total cost of 210 in 0.0 seconds
Search nodes expanded: 549
Pacman emerges victorious! Score: 300

[openMaze - DFS]
Path found with total cost of 298 in 0.0 seconds
Search nodes expanded: 576
Pacman emerges victorious! Score: 212

[openMaze - BFS]
Path found with total cost of 54 in 0.0 seconds
Search nodes expanded: 682
Pacman emerges victorious! Score: 456

[openMaze - UCS]
Path found with total cost of 54 in 0.0 seconds
Search nodes expanded: 682
Pacman emerges victorious! Score: 456

[openMaze - A* Manhattan]
Path found with total cost of 54 in 0.0 seconds
Search nodes expanded: 535
Pacman emerges victorious! Score: 456
```

### 4.3 Observations & Critical Analysis
- **Node Reduction on `bigMaze`**: A* with `manhattanHeuristic` expands **549** nodes (compared to **620** for BFS/UCS) while finding the optimal path of cost **210**.
- **Behavior on `openMaze`**:
  - **DFS**: Wanders around the open space, producing an extremely long, sub-optimal path of cost **298** (576 nodes expanded).
  - **BFS / UCS**: Expands in concentric circles in all directions, expanding **682** nodes to find the optimal path of cost **54**.
  - **A***: Uses Manhattan heuristic to focus search direction towards the goal, expanding only **535** nodes to find the optimal path of cost **54**.

---

## Question 5: Finding All the Corners (`CornersProblem`)

### 5.1 Commands Executed
```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

### 5.2 Console Output & Statistics
```text
[SearchAgent] using function bfs
[SearchAgent] using problem type CornersProblem
Path found with total cost of 28 in 0.0 seconds
Search nodes expanded: 252
Pacman emerges victorious! Score: 512

[SearchAgent] using function bfs
[SearchAgent] using problem type CornersProblem
Path found with total cost of 106 in 0.0 seconds
Search nodes expanded: 1966
Pacman emerges victorious! Score: 434
```

### 5.3 Observations & Critical Analysis
- **State Representation**: Formulated compactly as `((x, y), (visited_c0, visited_c1, visited_c2, visited_c3))`. This abstract state avoids embedding full `GameState` information, ensuring fast hashing and state space efficiency.
- **Verification Metrics**: 
  - `tinyCorners`: Path cost = **28** (matches expectation of ~28 steps).
  - `mediumCorners`: BFS expands **1,966** nodes to find the optimal path of length **106** (matches expectation of < 2,000 nodes).

---

## Question 6: Corners Heuristic (`cornersHeuristic`)

### 6.1 Command Executed
```bash
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

### 6.2 Console Output & Statistics
```text
Path found with total cost of 106 in 0.0 seconds
Search nodes expanded: 741
Pacman emerges victorious! Score: 434
```

### 6.3 Observations & Critical Analysis
- **Heuristic Design**: Evaluates the minimum total Manhattan distance to visit all remaining unvisited corners over all $k!$ permutations of unvisited corner visiting sequences starting from Pac-Man's current position $(x, y)$.
- **Admissibility & Consistency**: Because Manhattan distance is a lower bound on actual grid maze distance, taking the minimum over all permutations yields a strictly admissible and consistent lower bound.
- **Rubric Performance Tier**: Expands **741** nodes, placing it in the top performance bracket ($< 800$ nodes: "Doing great!").

---

## Question 7: Eating All The Dots (`foodHeuristic`)

### 7.1 Commands Executed
```bash
python pacman.py -l testSearch -p AStarFoodSearchAgent
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

### 7.2 Console Output & Statistics
```text
Path found with total cost of 7 in 0.0 seconds
Search nodes expanded: 10
Pacman emerges victorious! Score: 513

Path found with total cost of 60 in 0.3 seconds
Search nodes expanded: 4137
Pacman emerges victorious! Score: 570
```

### 7.3 Observations & Critical Analysis
- **Heuristic Design**: Calculates the maximum true maze distance (`mazeDistance`) from Pac-Man's current position $(x, y)$ to any remaining food dot in `foodGrid`, caching computed distances in `problem.heuristicInfo['distances']`.
- **Admissibility & Consistency**:
  - **Admissibility**: $h(s) = \max_{f \in \text{food}} \text{mazeDistance}(pos, f) \le h^*(s)$ because Pac-Man must visit all remaining dots, including the farthest one.
  - **Consistency**: Moving 1 step changes distance to any dot by at most 1, satisfying $h(s) - h(s') \le c(s, a, s') = 1$.
- **Rubric Performance & Extra Credit**:
  - `testSearch`: Cost = **7** (optimal), 10 nodes expanded.
  - `trickySearch`: Cost = **60** (optimal), **4,137** search nodes expanded in **0.3s** (substantially under the 7,000 threshold for **+5 Extra Credit**!).

