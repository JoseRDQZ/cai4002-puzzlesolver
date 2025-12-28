"""
Heuristics for A* search on 8-puzzle.
"""
from __future__ import annotations
from .state import State, IDX_TO_POS

def manhattan(state: State, goal: State) -> int:
    """Sum of Manhattan distances of tiles from their goal positions (ignore 0)."""
    pos_goal = {tile: i for i, tile in enumerate(goal)}
    dist = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        gi = pos_goal[tile]
        r1, c1 = IDX_TO_POS[i]
        r2, c2 = IDX_TO_POS[gi]
        dist += abs(r1 - r2) + abs(c1 - c2)
    return dist

def misplaced_tiles(state: State, goal: State) -> int:
    """Count tiles not in their goal positions (ignore 0)."""
    return sum(1 for i, t in enumerate(state) if t != 0 and t != goal[i])

# --- Bonus: Linear Conflict (admissible) ---
# H = Manhattan + 2 * (# of linear conflicts)

def _goal_pos_map(goal: State):
    return {tile: i for i, tile in enumerate(goal)}

def _row_conflicts(state: State, goal_map) -> int:
    conflicts = 0
    for row in range(3):
        # tiles currently in this row whose goal row is also this row
        tiles = []
        for col in range(3):
            idx = row * 3 + col
            t = state[idx]
            if t == 0:
                continue
            gi = goal_map[t]
            gr, gc = gi // 3, gi % 3
            if gr == row:
                tiles.append((col, gc))  # (current_col, goal_col)
        # count inversions by goal_col within this row
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                # if two tiles are in the same row and "cross" wrt their goal columns, that's a conflict
                if tiles[i][1] > tiles[j][1]:
                    conflicts += 1
    return conflicts

def _col_conflicts(state: State, goal_map) -> int:
    conflicts = 0
    for col in range(3):
        tiles = []
        for row in range(3):
            idx = row * 3 + col
            t = state[idx]
            if t == 0:
                continue
            gi = goal_map[t]
            gr, gc = gi // 3, gi % 3
            if gc == col:
                tiles.append((row, gr))  # (current_row, goal_row)
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i][1] > tiles[j][1]:
                    conflicts += 1
    return conflicts

def manhattan_linear_conflict(state: State, goal: State) -> int:
    goal_map = _goal_pos_map(goal)
    base = manhattan(state, goal)
    lc = _row_conflicts(state, goal_map) + _col_conflicts(state, goal_map)
    return base + 2 * lc
