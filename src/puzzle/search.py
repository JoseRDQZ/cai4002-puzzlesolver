"""
A* (required), plus optional BFS/DFS for comparison.
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Callable, Set, Deque
from collections import deque
import heapq

from .state import State, neighbors, GOAL
from . import heuristics as H

HeuristicFn = Callable[[State, State], int]

def _reconstruct_moves(parents: Dict[State, Tuple[Optional[State], str]], goal: State) -> List[str]:
    moves: List[str] = []
    cur = goal
    while True:
        parent, move = parents[cur]
        if parent is None:
            break
        moves.append(move)
        cur = parent
    moves.reverse()
    return moves

def a_star(start: State, goal: State = GOAL, heuristic: HeuristicFn = H.manhattan) -> Dict:
    """
    Return dict with keys: moves, cost, expanded, states.
    Uses g(n)+h(n) with default heuristic = Manhattan.
    """
    if start == goal:
        return {"moves": [], "cost": 0, "expanded": 0, "states": [start]}

    open_heap: List[Tuple[int, int, State]] = []
    g: Dict[State, int] = {start: 0}
    parents: Dict[State, Tuple[Optional[State], str]] = {start: (None, '')}
    expanded = 0
    entry_id = 0

    heapq.heappush(open_heap, (heuristic(start, goal), entry_id, start)); entry_id += 1
    closed: Set[State] = set()

    while open_heap:
        _, _, s = heapq.heappop(open_heap)
        if s in closed:
            continue
        closed.add(s)
        expanded += 1

        if s == goal:
            moves = _reconstruct_moves(parents, s)
            # reconstruct states for convenience
            states = [start]
            cur = start
            for mv in moves:
                for ns, m in neighbors(cur):
                    if m == mv:
                        states.append(ns); cur = ns; break
            return {"moves": moves, "cost": len(moves), "expanded": expanded, "states": states}

        for ns, mv in neighbors(s):
            tentative = g[s] + 1
            if ns not in g or tentative < g[ns]:
                g[ns] = tentative
                parents[ns] = (s, mv)
                f = tentative + heuristic(ns, goal)
                heapq.heappush(open_heap, (f, entry_id, ns)); entry_id += 1

    raise RuntimeError("A* failed to find a path (shouldn't happen for solvable puzzles).")

def bfs(start: State, goal: State = GOAL) -> Dict:
    if start == goal:
        return {"moves": [], "cost": 0, "expanded": 0, "states": [start]}
    q: Deque[State] = deque([start])
    parents: Dict[State, Tuple[Optional[State], str]] = {start: (None, '')}
    seen: Set[State] = {start}
    expanded = 0

    while q:
        s = q.popleft()
        expanded += 1
        if s == goal:
            moves = _reconstruct_moves(parents, s)
            states = [start]
            cur = start
            for mv in moves:
                for ns, m in neighbors(cur):
                    if m == mv:
                        states.append(ns); cur = ns; break
            return {"moves": moves, "cost": len(moves), "expanded": expanded, "states": states}
        for ns, mv in neighbors(s):
            if ns not in seen:
                seen.add(ns)
                parents[ns] = (s, mv)
                q.append(ns)

    raise RuntimeError("BFS failed to find a path (shouldn't happen for solvable puzzles).")

def dfs(start: State, goal: State = GOAL, depth_limit: int = 50) -> Dict:
    """Naive DFS with depth limit (for comparison only)."""
    stack: List[Tuple[State, int]] = [(start, 0)]
    parents: Dict[State, Tuple[Optional[State], str]] = {start: (None, '')}
    seen: Set[State] = {start}
    expanded = 0

    while stack:
        s, d = stack.pop()
        expanded += 1
        if s == goal:
            moves = _reconstruct_moves(parents, s)
            states = [start]
            cur = start
            for mv in moves:
                for ns, m in neighbors(cur):
                    if m == mv:
                        states.append(ns); cur = ns; break
            return {"moves": moves, "cost": len(moves), "expanded": expanded, "states": states}
        if d < depth_limit:
            for ns, mv in neighbors(s):
                if ns not in seen:
                    seen.add(ns)
                    parents[ns] = (s, mv)
                    stack.append((ns, d + 1))

    raise RuntimeError("DFS depth-limited search did not reach the goal.")
