# Additions to the report

## Memory usage

Memory was measured with `tracemalloc`.
The values show **peak traced Python allocations during search**

| Search | Layout / Input | Problem | Peak memory (MiB) |
| --- | --- | --- | ---: |
| DFS | tinyMaze | Position | 0.003830 |
| DFS | mediumMaze | Position | 0.030151 |
| DFS | bigMaze | Position | 0.114052 |
| BFS | mediumMaze | Position | 0.038132 |
| BFS | bigMaze | Position | 0.100830 |
| BFS | Fixed 8-puzzle | Puzzle | 0.006637 |
| UCS | mediumMaze | Position | 0.039192 |
| UCS | mediumDottedMaze | StayEast | 0.035271 |
| UCS | mediumScaryMaze | StayWest | 0.031200 |
| A* | bigMaze | Position | 0.100372 |
| DFS | openMaze | Position | 0.549309 |
| BFS | openMaze | Position | 0.104294 |
| UCS | openMaze | Position | 0.109413 |
| A* | openMaze | Position | 0.101685 |
| BFS | tinyCorners | Corners | 0.063950 |
| BFS | mediumCorners | Corners | 0.534843 |
| A* | mediumCorners | Corners | 0.194038 |
| A* | testSearch | Food | 0.014252 |
| A* | trickySearch | Food | 12.379196 |


**Add to the conclusion:** On `mediumCorners`, A* used less peak memory than BFS while finding the same optimal path. On `openMaze`, DFS used more memory than BFS despite expanding fewer nodes. Expanded-node count alone therefore does not determine memory usage. `trickySearch` had the largest measured peak, including food-grid states and cached maze distances.

## Short explanation to add for Q6

The corners heuristic checks all orders of the remaining corners and chooses the smallest sum of Manhattan distances. Ignoring walls cannot increase the shortest remaining route, so the heuristic is admissible. Taking one step and then following the next state's best relaxed route gives `h(s) <= 1 + h(s')`, so it is consistent. It returns zero when all corners are visited.
