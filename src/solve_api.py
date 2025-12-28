"""
solve_api.py
------------
Alex — this is the easy interface for you to plug the solver into your UI.

Call `shuffle_start()` to get a solvable starting board.
Call `solve()` to solve any board you give it.

Format:
- Board = list of 9 ints, with 0 as the blank.
- Order is row-major:

  0 1 2
  3 4 5
  6 7 8
"""

from __future__ import annotations
from typing import List, Literal, Tuple, Optional

from .puzzle.state import GOAL, shuffle as _shuffle, neighbors as _neighbors
from .puzzle.search import a_star, bfs, dfs
from .puzzle import heuristics as H

Algo = Literal["astar", "bfs", "dfs"]
Heur = Literal["manhattan", "misplaced", "manhattan_linear_conflict"]

_HEURS = {
    "manhattan": H.manhattan,
    "misplaced": H.misplaced_tiles,
    "manhattan_linear_conflict": getattr(H, "manhattan_linear_conflict", H.manhattan),
}


def _ensure_non_goal(state: Tuple[int, ...]) -> Tuple[int, ...]:
    # Makes sure the shuffled state isn’t already solved
    if state == GOAL:
        s = _shuffle(GOAL, depth=41, seed=None)
        if s == GOAL:
            s, _ = _neighbors(s)[0]
        return s
    return state


def shuffle_start(depth: int = 40, seed: Optional[int] = None) -> List[int]:
    """Alex — call this to get a random solvable 8-puzzle board as a flat list of 9 numbers."""
    s = _shuffle(GOAL, depth=depth, seed=seed)
    s = _ensure_non_goal(s)
    return list(s)


def is_valid_state(state: List[int], require_solvable: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Use this if you want to double-check the board you have is valid and solvable.
    """
    if len(state) != 9:
        return False, "State must have 9 numbers."
    if sorted(state) != list(range(9)):
        return False, "State must contain numbers 0..8 exactly once."
    if require_solvable:
        from src.puzzle.state import is_solvable
        if not is_solvable(tuple(state)):
            return False, "State is not solvable."
    return True, None


def solve(start: List[int], algo: Algo = "astar",
          heuristic: Heur = "manhattan", depth_limit: int = 50) -> dict:
    """
    Alex — this solves the puzzle from any given board.

    Returns a dict like:
    {
        "moves": ["U","R","D",...],
        "states": [ [...9 ints...], [...], ... ],
        "cost": <steps>,
        "expanded": <nodes explored>
    }

    You can just loop through result["states"] to animate the solution.
    """
    ok, err = is_valid_state(start, require_solvable=(algo != "dfs"))
    if not ok:
        raise ValueError(f"Invalid state: {err}")

    s = tuple(start)
    if algo == "astar":
        res = a_star(s, GOAL, heuristic=_HEURS[heuristic])
    elif algo == "bfs":
        res = bfs(s, GOAL)
    else:
        res = dfs(s, GOAL, depth_limit=depth_limit)

    return {
        "moves": res["moves"],
        "states": [list(t) for t in res["states"]],
        "cost": res["cost"],
        "expanded": res["expanded"],
    }
