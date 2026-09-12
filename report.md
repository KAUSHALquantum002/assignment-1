# CSE 537 - Artificial Intelligence: Assignment 1 Report

## Executive Summary

This report documents the implementation, empirical testing, and theoretical analysis of classical search algorithms applied to Pac-Man maze navigation and the 8-puzzle problem. The algorithms implemented in `search.py` include:
1. **Depth-First Search (DFS)** - Uninformed LIFO Graph Search
2. **Breadth-First Search (BFS)** - Uninformed FIFO Graph Search
3. **Uniform-Cost Search (UCS)** - Priority-based Graph Search by path cost $g(n)$
4. **A* Search** - Informed Graph Search by $f(n) = g(n) + h(n)$

---

## Overall Performance Summary Table

| Question | Algorithm | Layout / Problem | Heuristic / Cost Function | Solution Cost | Nodes Expanded | Optimal? |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Q1** | DFS | `tinyMaze` | Uniform ($1$) | 10 | 15 | No |
| **Q1** | DFS | `mediumMaze` | Uniform ($1$) | 130 | 146 | No |
| **Q1** | DFS | `bigMaze` | Uniform ($1$) | 210 | 390 | No |
| **Q2** | BFS | `mediumMaze` | Uniform ($1$) | **68** | 269 | **Yes** |
| **Q2** | BFS | `bigMaze` | Uniform ($1$) | **210** | 620 | **Yes** |
| **Q2** | BFS | `eightpuzzle.py` | Uniform ($1$) | 1 | N/A | **Yes** |
| **Q3** | UCS | `mediumMaze` | `SearchAgent` (Uniform) | **68** | 269 | **Yes** |
| **Q3** | UCS | `mediumDottedMaze` | `StayEastSearchAgent` ($2^x$) | **1** | 186 | **Yes** |
| **Q3** | UCS | `mediumScaryMaze` | `StayWestSearchAgent` ($2^x$) | **68,719,479,864** | 108 | **Yes** |
| **Q4** | A* | `bigMaze` | `manhattanHeuristic` | **210** | **549** | **Yes** |
| **Q4** | A* | `openMaze` | `manhattanHeuristic` | **54** | **535** | **Yes** |

---

## Question 1: Depth-First Search (DFS)

### 1.1 Description
Graph-Search Depth-First Search explores the deepest nodes in the search tree first. To prevent infinite loops in graphs with cycles, expanded states are tracked in a `visited` set.

### 1.2 Implementation
Implemented in `depthFirstSearch` in `search.py` using `util.Stack()`:

```python
def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.
    """
    fringe = util.Stack()
    start_state = problem.getStartState()
    fringe.push((start_state, []))
    visited = set()

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    fringe.push((successor, actions + [action]))

    return []
```

### 1.3 Empirical Results
- **`tinyMaze`**: Cost = **10**, Nodes Expanded = **15**
- **`mediumMaze`**: Cost = **130**, Nodes Expanded = **146**
- **`bigMaze`**: Cost = **210**, Nodes Expanded = **390**

### 1.4 Conceptual Questions & Answers
1. **Is the exploration order what you would have expected?**
   - **Yes.** DFS expands deep along a single branch before backtracking. Because `util.Stack` is LIFO, pushing successors `[North, South, East, West]` causes `West` to be popped and explored first.
2. **Does Pac-Man actually go to all the explored squares on its way to the goal?**
   - **No.** Explored red squares represent states evaluated in search space during the algorithm's execution. Pac-Man physically travels only along the final returned solution path.
3. **Is this a least-cost solution? If not, think about what depth-first search is doing wrong.**
   - **No.** DFS is not optimal because it returns the first path it finds reaching the goal, regardless of path length or step costs.

---

## Question 2: Breadth-First Search (BFS)

### 2.1 Description
Graph-Search Breadth-First Search expands the shallowest nodes in the search tree first using a First-In-First-Out (FIFO) queue.

### 2.2 Implementation
Implemented in `breadthFirstSearch` in `search.py` using `util.Queue()`:

```python
def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    fringe = util.Queue()
    start_state = problem.getStartState()
    fringe.push((start_state, []))
    visited = set()

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    fringe.push((successor, actions + [action]))

    return []
```

### 2.3 Empirical Results
- **`mediumMaze`**: Cost = **68** (Optimal), Nodes Expanded = **269**
- **`bigMaze`**: Cost = **210** (Optimal), Nodes Expanded = **620**
- **`eightpuzzle.py`**: Solved 8-puzzle instance correctly in 1 move (`['up']`).

### 2.4 Conceptual Questions & Answers
1. **Does BFS find a least-cost solution?**
   - **Yes.** When all edge step costs are equal (uniform cost = 1), path depth equals path cost. Since BFS explores level-by-level, the first time a goal state is dequeued, it is guaranteed to be reached via the shortest/least-cost path.

---

## Question 3: Uniform-Cost Search (UCS)

### 3.1 Description
Uniform-Cost Search (Dijkstra's algorithm) expands nodes in order of increasing cumulative path cost $g(n)$ using a priority queue.

### 3.2 Implementation
Implemented in `uniformCostSearch` in `search.py` using `util.PriorityQueue()`:

```python
def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    fringe = util.PriorityQueue()
    start_state = problem.getStartState()
    fringe.push((start_state, [], 0), 0)
    visited = set()

    while not fringe.isEmpty():
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    new_cost = cost + stepCost
                    fringe.push((successor, actions + [action], new_cost), new_cost)

    return []
```

### 3.3 Empirical Results
- **`mediumMaze` (`fn=ucs`)**: Cost = **68** (Optimal), Nodes Expanded = **269**
- **`mediumDottedMaze` (`StayEastSearchAgent`)**: Cost = **1**, Nodes Expanded = **186**
- **`mediumScaryMaze` (`StayWestSearchAgent`)**: Cost = **68,719,479,864**, Nodes Expanded = **108**

---

## Question 4: A* Search

### 4.1 Description
A* Graph Search expands nodes in order of increasing $f(n) = g(n) + h(n)$, combining actual path cost $g(n)$ with a heuristic estimate $h(n)$ to guide search towards the goal efficiently.

### 4.2 Implementation
Implemented in `aStarSearch` in `search.py` using `util.PriorityQueue()`:

```python
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    fringe = util.PriorityQueue()
    start_state = problem.getStartState()
    fringe.push((start_state, [], 0), 0 + heuristic(start_state, problem))
    visited = set()

    while not fringe.isEmpty():
        state, actions, cost = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    new_cost = cost + stepCost
                    priority = new_cost + heuristic(successor, problem)
                    fringe.push((successor, actions + [action], new_cost), priority)

    return []
```

### 4.3 Empirical Results & `openMaze` Comparison
- **`bigMaze` (`manhattanHeuristic`)**: Cost = **210** (Optimal), Nodes Expanded = **549** (vs 620 for UCS)

#### Strategy Comparison on `openMaze`:
| Strategy | Solution Cost | Search Nodes Expanded | Behavior / Analysis |
| :--- | :---: | :---: | :--- |
| **DFS** | 298 | 576 | Wanders extensively through open space, returning a highly sub-optimal path (cost 298). |
| **BFS** | 54 | 682 | Finds the optimal path (cost 54), expanding nodes uniformly in all directions (concentric wave). |
| **UCS** | 54 | 682 | Identical to BFS because edge step costs are uniform ($1$). |
| **A\*** (`manhattanHeuristic`) | **54** | **535** | Finds the optimal path while expanding significantly fewer nodes (**535** vs **682**) by directing search towards the goal. |

