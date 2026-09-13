# CSE 537 - Artificial Intelligence: Assignment 1 Report

## Executive Summary

This report documents the implementation, empirical testing, and theoretical analysis of classical search algorithms applied to Pac-Man maze navigation and the 8-puzzle problem. The algorithms implemented in `search.py` and `searchAgents.py` include:
1. **Depth-First Search (DFS)** - Uninformed LIFO Graph Search
2. **Breadth-First Search (BFS)** - Uninformed FIFO Graph Search
3. **Uniform-Cost Search (UCS)** - Priority-based Graph Search by path cost $g(n)$
4. **A* Search** - Informed Graph Search by $f(n) = g(n) + h(n)$
5. **CornersProblem State Formulation** - Abstract search space encoding Pac-Man's position and visited corner states.
6. **CornersProblem Heuristic (`cornersHeuristic`)** - Permutation-based minimum Manhattan path lower bound.
7. **FoodSearchProblem Heuristic (`foodHeuristic`)** - Cached maximum maze-distance heuristic for eating all food dots.

---

## Overall Performance Summary Table

| Question | Algorithm | Layout / Problem | Heuristic / Cost Function | Solution Cost | Nodes Expanded | Optimal? | Grading Tier / Extra Credit |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Q1** | DFS | `tinyMaze` | Uniform ($1$) | 10 | 15 | No | N/A |
| **Q1** | DFS | `mediumMaze` | Uniform ($1$) | 130 | 146 | No | N/A |
| **Q1** | DFS | `bigMaze` | Uniform ($1$) | 210 | 390 | No | N/A |
| **Q2** | BFS | `mediumMaze` | Uniform ($1$) | **68** | 269 | **Yes** | N/A |
| **Q2** | BFS | `bigMaze` | Uniform ($1$) | **210** | 620 | **Yes** | N/A |
| **Q2** | BFS | `eightpuzzle.py` | Uniform ($1$) | 1 | N/A | **Yes** | N/A |
| **Q3** | UCS | `mediumMaze` | `SearchAgent` (Uniform) | **68** | 269 | **Yes** | N/A |
| **Q3** | UCS | `mediumDottedMaze` | `StayEastSearchAgent` ($2^x$) | **1** | 186 | **Yes** | N/A |
| **Q3** | UCS | `mediumScaryMaze` | `StayWestSearchAgent` ($2^x$) | **68,719,479,864** | 108 | **Yes** | N/A |
| **Q4** | A* | `bigMaze` | `manhattanHeuristic` | **210** | **549** | **Yes** | N/A |
| **Q4** | A* | `openMaze` | `manhattanHeuristic` | **54** | **535** | **Yes** | N/A |
| **Q5** | BFS | `tinyCorners` | `CornersProblem` | **28** | 252 | **Yes** | N/A |
| **Q5** | BFS | `mediumCorners` | `CornersProblem` | **106** | 1,966 | **Yes** | N/A |
| **Q6** | A* | `mediumCorners` | `cornersHeuristic` | **106** | **741** | **Yes** | **Top Tier (< 800)** |
| **Q7** | A* | `testSearch` | `foodHeuristic` | **7** | 10 | **Yes** | N/A |
| **Q7** | A* | `trickySearch` | `foodHeuristic` | **60** | **4,137** | **Yes** | **Extra Credit (< 7,000)** |

---

## Question 1: Depth-First Search (DFS)

### 1.1 Description
Graph-Search Depth-First Search explores the deepest nodes in the search tree first. To prevent infinite loops in graphs with cycles, expanded states are tracked in a `visited` set.

### 1.2 Implementation
Implemented in `depthFirstSearch` in `search.py` using `util.Stack()`:

```python
def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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

---

## Question 2: Breadth-First Search (BFS)

### 2.1 Description
Graph-Search Breadth-First Search expands the shallowest nodes in the search tree first using a First-In-First-Out (FIFO) queue.

### 2.2 Implementation
Implemented in `breadthFirstSearch` in `search.py` using `util.Queue()`:

```python
def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
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

---

## Question 3: Uniform-Cost Search (UCS)

### 3.1 Description
Uniform-Cost Search (Dijkstra's algorithm) expands nodes in order of increasing cumulative path cost $g(n)$ using a priority queue.

### 3.2 Implementation
Implemented in `uniformCostSearch` in `search.py` using `util.PriorityQueue()`:

```python
def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
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

---

## Question 4: A* Search

### 4.1 Description
A* Graph Search expands nodes in order of increasing $f(n) = g(n) + h(n)$, combining actual path cost $g(n)$ with a heuristic estimate $h(n)$ to guide search towards the goal efficiently.

### 4.2 Implementation
Implemented in `aStarSearch` in `search.py` using `util.PriorityQueue()`:

```python
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
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

---

## Question 5: CornersProblem State Formulation

### 5.1 Description
The `CornersProblem` requires Pac-Man to find the shortest path visiting all 4 corners of a layout. 

### 5.2 Abstract State Space Selection
State representation:
$$\text{state} = \big((x, y), \, (c_0, c_1, c_2, c_3)\big)$$

---

## Question 6: CornersProblem Heuristic (`cornersHeuristic`)

### 6.1 Description
To achieve optimal search node reduction while guaranteeing admissibility, `cornersHeuristic` computes the minimum total Manhattan distance required to visit all remaining unvisited corners over all possible permutations of corner visiting orders.

### 6.2 Implementation
Implemented inside `cornersHeuristic` in `searchAgents.py`:

```python
def cornersHeuristic(state: Any, problem: CornersProblem):
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    position, visited = state
    unvisited = [corner for corner, is_visited in zip(corners, visited) if not is_visited]

    if not unvisited:
        return 0

    import itertools
    min_dist = float('inf')
    for perm in itertools.permutations(unvisited):
        dist = util.manhattanDistance(position, perm[0])
        for i in range(len(perm) - 1):
            dist += util.manhattanDistance(perm[i], perm[i+1])
        if dist < min_dist:
            min_dist = dist

    return min_dist
```

---

## Question 7: FoodSearchProblem Heuristic (`foodHeuristic`)

### 7.1 Description
For `FoodSearchProblem`, `foodHeuristic` calculates the maximum true maze distance (`mazeDistance`) from Pac-Man's current position to any remaining food dot in `foodGrid`. To ensure fast evaluation, computed maze distances are cached in `problem.heuristicInfo['distances']`.

### 7.2 Proof of Admissibility & Consistency
- **Admissibility**: Pac-Man must visit all remaining food dots, including the one that is farthest away in terms of maze distance. Therefore, $\max_{f \in \text{food}} \text{mazeDistance}(pos, f)$ is a strict lower bound on the true distance required to eat all food dots ($h(s) \le h^*(s)$).
- **Consistency**: Moving one step changes Pac-Man's maze distance to any food dot by at most $1$. Thus, $h(s) - h(s') \le 1 = c(s, a, s')$, satisfying consistency.

### 7.3 Implementation
Implemented in `foodHeuristic` in `searchAgents.py`:

```python
def foodHeuristic(state: Tuple[Tuple, List[List]], problem: FoodSearchProblem):
    position, foodGrid = state
    food_list = foodGrid.asList()

    if not food_list:
        return 0

    if 'distances' not in problem.heuristicInfo:
        problem.heuristicInfo['distances'] = {}

    distances = problem.heuristicInfo['distances']

    max_dist = 0
    for food in food_list:
        key = (position, food)
        if key not in distances:
            distances[key] = mazeDistance(position, food, problem.startingGameState)
        dist = distances[key]
        if dist > max_dist:
            max_dist = dist

    return max_dist
```

### 7.4 Verification Results
- **`testSearch`**: Solution Cost = **7**, Search Nodes Expanded = **10**
- **`trickySearch`**: Solution Cost = **60**, Search Nodes Expanded = **4,137** (Substantially under the 7,000 threshold, qualifying for **+5 Extra Credit**!)
