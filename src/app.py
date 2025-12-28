"""
Part A demo + bonus compare.
- Prints a shuffled start and solves with A* (Manhattan+LC by default).
- Then benchmarks A*, BFS, DFS on the same start (cost, expanded, runtime).
"""

from __future__ import annotations
import time

try:
    from puzzle.state import GOAL, shuffle, to_grid
    from puzzle.search import a_star, bfs, dfs
    from puzzle import heuristics as H
except Exception:
    import sys, os
    here = os.path.dirname(__file__)
    sys.path.append(os.path.dirname(here))
    from puzzle.state import GOAL, shuffle, to_grid
    from puzzle.search import a_star, bfs, dfs
    from puzzle import heuristics as H


def print_board(state):
    grid = to_grid(state)
    for row in grid:
        print(" ".join("{:>2}".format(x) if x != 0 else "  " for x in row))
    print()


def build_non_goal_start(depth_primary: int = 40, depth_secondary: int = 41):
    from puzzle.state import neighbors
    start = shuffle(GOAL, depth=depth_primary, seed=None)
    if start == GOAL:
        start = shuffle(GOAL, depth=depth_secondary, seed=None)
        if start == GOAL:
            start, _ = neighbors(start)[0]
    return start


def compare_algorithms(start):
    print("\n=== Algorithm comparison on the same start ===")

    # A* with different heuristics
    for name, h in [
        ("A* Manhattan", H.manhattan),
        ("A* Manhattan+LinearConflict", getattr(H, "manhattan_linear_conflict", H.manhattan)),
    ]:
        t0 = time.perf_counter()
        res = a_star(start, GOAL, heuristic=h)
        dt = (time.perf_counter() - t0) * 1000
        print(f"{name:>28}: cost={res['cost']:>2} | expanded={res['expanded']:>4} | time={dt:6.2f} ms")

    # BFS (optimal but usually expands a lot)
    t0 = time.perf_counter()
    res_bfs = bfs(start, GOAL)
    dt = (time.perf_counter() - t0) * 1000
    print(f"{'BFS':>28}: cost={res_bfs['cost']:>2} | expanded={res_bfs['expanded']:>4} | time={dt:6.2f} ms")

    # DFS (depth-limited; not guaranteed optimal, may fail if limit too low)
    try:
        t0 = time.perf_counter()
        res_dfs = dfs(start, GOAL, depth_limit=50)
        dt = (time.perf_counter() - t0) * 1000
        print(f"{'DFS (limit=50)':>28}: cost={res_dfs['cost']:>2} | expanded={res_dfs['expanded']:>4} | time={dt:6.2f} ms")
    except Exception as e:
        print(f"{'DFS (limit=50)':>28}: failed ({e})")


def main():
    print("8-Puzzle — Part A demo (with bonus)")

    # use the stronger heuristic by default for the main solve
    heuristic = getattr(H, "manhattan_linear_conflict", H.manhattan)

    start = build_non_goal_start()
    print("Start:")
    print_board(start)

    print("Goal:")
    print_board(GOAL)

    print("Solving with A* ...")
    res = a_star(start, GOAL, heuristic=heuristic)
    print(f"Moves: {''.join(res['moves'])}")
    print(f"Cost (steps): {res['cost']} | Expanded: {res['expanded']}")
    print("First few states:")
    for i, s in enumerate(res['states'][:5]):
        print(f"Step {i}:")
        print_board(s)

    # Bonus: quick comparison table
    compare_algorithms(start)


if __name__ == "__main__":
    main()
