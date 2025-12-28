"""
State representation and helpers for 8-puzzle (3x3).

- A state is a 9-int tuple with values 0..8 (0 = blank).
- Default goal: (1,2,3,4,5,6,7,8,0)
"""
from __future__ import annotations
from typing import Iterable, List, Tuple, Optional
import random

State = Tuple[int, ...]
Move = str  # 'U','D','L','R'

GOAL: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)
IDX_TO_POS = {i: (i // 3, i % 3) for i in range(9)}
POS_TO_IDX = {(r, c): 3 * r + c for r in range(3) for c in range(3)}


def to_grid(state: State) -> List[List[int]]:
    return [list(state[i:i + 3]) for i in range(0, 9, 3)]


def from_grid(grid: List[List[int]]) -> State:
    flat: List[int] = []
    for row in grid:
        flat.extend(row)
    return tuple(flat)


def blank_index(state: State) -> int:
    return state.index(0)


def swap(state: State, i: int, j: int) -> State:
    lst = list(state)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)


def neighbors(state: State) -> List[Tuple[State, Move]]:
    """
    Return neighbors and the move taken ('U','D','L','R') applied to the blank.
    Move = direction the BLANK moves.
    """
    i = blank_index(state)
    r, c = IDX_TO_POS[i]
    out: List[Tuple[State, Move]] = []

    if r > 0:  # Up
        j = POS_TO_IDX[(r - 1, c)]
        out.append((swap(state, i, j), 'U'))
    if r < 2:  # Down
        j = POS_TO_IDX[(r + 1, c)]
        out.append((swap(state, i, j), 'D'))
    if c > 0:  # Left
        j = POS_TO_IDX[(r, c - 1)]
        out.append((swap(state, i, j), 'L'))
    if c < 2:  # Right
        j = POS_TO_IDX[(r, c + 1)]
        out.append((swap(state, i, j), 'R'))

    return out


def inversion_count(state: State) -> int:
    seq = [x for x in state if x != 0]
    inv = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inv += 1
    return inv


def is_solvable(state: State) -> bool:
    """For 3x3, solvable iff inversion count is even."""
    return inversion_count(state) % 2 == 0


def shuffle(goal: State = GOAL, depth: int = 50, seed: Optional[int] = None) -> State:
    """
    Generate a solvable puzzle by random legal moves from goal.
    depth: number of random moves.
    """
    rng = random.Random(seed)
    s = goal
    prev = None
    for _ in range(depth):
        neigh = neighbors(s)
        if prev is not None:  # avoid instantly undoing the last move
            neigh = [n for n in neigh if n[0] != prev]
        s, _ = rng.choice(neigh)
        prev = s
    return s


def apply_moves(start: State, moves: Iterable[Move]) -> Iterable[State]:
    s = start
    yield s
    for m in moves:
        for ns, mv in neighbors(s):
            if mv == m:
                s = ns
                break
        else:
            raise ValueError(f"Invalid move '{m}' from state {s}")
        yield s
