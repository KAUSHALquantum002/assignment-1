"""Measure peak Python memory for the 19 cases in our report."""
import gc
from pathlib import Path
import sys
import tracemalloc

sys.dont_write_bytecode = True
project = Path.cwd()
sys.path.insert(0, str(project))
import eightpuzzle
import layout
import pacman
import search
import searchAgents

tests = [
    ("tinyMaze", "dfs", "position"),
    ("mediumMaze", "dfs", "position"),
    ("bigMaze", "dfs", "position"),
    ("mediumMaze", "bfs", "position"),
    ("bigMaze", "bfs", "position"),
    ("fixed-puzzle", "bfs", "puzzle"),
    ("mediumMaze", "ucs", "position"),
    ("mediumDottedMaze", "ucs", "east"),
    ("mediumScaryMaze", "ucs", "west"),
    ("bigMaze", "astar", "position"),
    ("openMaze", "dfs", "position"),
    ("openMaze", "bfs", "position"),
    ("openMaze", "ucs", "position"),
    ("openMaze", "astar", "position"),
    ("tinyCorners", "bfs", "corners"),
    ("mediumCorners", "bfs", "corners"),
    ("mediumCorners", "astar", "corners"),
    ("testSearch", "astar", "food"),
    ("trickySearch", "astar", "food"),
]

print("Peak traced Python memory during search.")
print(f"{'Maze':<18} {'Search':<6} {'Problem':<8} {'Moves':>5} {'Cost':>18} {'Nodes':>6} {'Peak MiB':>10}")

for maze, algorithm, kind in tests:
    # Prepare a new problem before starting memory tracking.
    heuristic = search.nullHeuristic
    if kind == "puzzle":
        # The supplied puzzle code reads this module-level variable.
        eightpuzzle.puzzle = eightpuzzle.EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8])
        problem = eightpuzzle.EightPuzzleSearchProblem(eightpuzzle.puzzle)
    else:
        maze_file = project / "layouts" / (maze + ".lay")
        state = pacman.GameState()
        state.initialize(layout.Layout(maze_file.read_text().splitlines()), 0)
        if kind == "corners":
            problem = searchAgents.CornersProblem(state)
            heuristic = searchAgents.cornersHeuristic
        elif kind == "food":
            problem = searchAgents.FoodSearchProblem(state)
            heuristic = searchAgents.foodHeuristic
        else:
            if kind == "east":
                cost = lambda position: 0.5 ** position[0]
            elif kind == "west":
                cost = lambda position: 2 ** position[0]
            else:
                cost = lambda position: 1
            problem = searchAgents.PositionSearchProblem(
                state, costFn=cost, warn=False, visualize=False
            )
            heuristic = searchAgents.manhattanHeuristic

    # Select dfs, bfs, ucs, or astar.
    search_function = getattr(search, algorithm)
    gc.collect()
    tracemalloc.start()
    try:
        if algorithm == "astar":
            actions = search_function(problem, heuristic=heuristic)
        else:
            actions = search_function(problem)
        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    peak_mib = peak_bytes / (1024 ** 2)
    nodes = getattr(problem, "_expanded", "N/A")
    path_cost = problem.getCostOfActions(actions)
    print(f"{maze:<18} {algorithm:<6} {kind:<8} {len(actions):>5} {path_cost:>18.12g} {str(nodes):>6} {peak_mib:>10.6f}")
