import unittest
from src.puzzle.state import GOAL, shuffle, is_solvable
from src.puzzle.search import a_star, bfs
from src.puzzle import heuristics as H

class TestPuzzleBonus(unittest.TestCase):
    def test_shuffle_is_solvable(self):
        s = shuffle(GOAL, depth=25, seed=7)
        self.assertTrue(is_solvable(s))

    def test_astar_reaches_goal(self):
        s = shuffle(GOAL, depth=15, seed=3)
        res = a_star(s, GOAL, heuristic=getattr(H, "manhattan_linear_conflict", H.manhattan))
        self.assertEqual(res["states"][-1], GOAL)

    def test_astar_cost_matches_bfs(self):
        s = shuffle(GOAL, depth=12, seed=11)
        a = a_star(s, GOAL, heuristic=H.manhattan)
        b = bfs(s, GOAL)
        self.assertEqual(a["cost"], b["cost"])

if __name__ == "__main__":
    unittest.main()
