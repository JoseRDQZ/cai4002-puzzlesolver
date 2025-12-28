"""
server.py
---------
Alex — if you want to make a web UI, you can call this as a local API.

Endpoints:
- GET /shuffle -> returns a solvable board
- POST /solve  -> solves the board you send

How to run:
- Start the "Run Solver API" config in VS Code (I’ll add it for you)
- Then open http://127.0.0.1:8000/docs to try the endpoints
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from src.solve_api import shuffle_start, solve as solve_fn, is_valid_state

app = FastAPI(title="8-Puzzle Solver API")

class SolveReq(BaseModel):
    start: List[int] = Field(..., min_length=9, max_length=9)
    algo: Literal["astar","bfs","dfs"] = "astar"
    heuristic: Literal["manhattan","misplaced","manhattan_linear_conflict"] = "manhattan"
    depth_limit: int = 50

@app.get("/shuffle")
def shuffle(depth: int = 40, seed: Optional[int] = None):
    return {"state": shuffle_start(depth=depth, seed=seed)}

@app.post("/solve")
def solve(req: SolveReq):
    ok, err = is_valid_state(req.start, require_solvable=(req.algo != "dfs"))
    if not ok:
        return {"error": err}
    return solve_fn(req.start, req.algo, req.heuristic, req.depth_limit)

from fastapi.staticfiles import StaticFiles
import os

root_dir = os.path.dirname(os.path.dirname(__file__))  # project root
static_dir = os.path.join(root_dir, "static")

if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")