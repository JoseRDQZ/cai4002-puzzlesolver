====================================================
8-Puzzle Solver
====================================================
Course: CAL 4002
Assignment: HW1
Authors: Jose Rodriguez and Alex Gomez
Date: September 2025

----------------------------------------------------
Overview
----------------------------------------------------
This project implements an 8-puzzle solver using search algorithms
(BFS, DFS, A*). It provides a FastAPI backend and a simple web
frontend where users can shuffle the puzzle, upload an image, and
see the puzzle solved automatically.

----------------------------------------------------
Requirements
----------------------------------------------------
Python 3.11+  
Install dependencies with:

    pip install -r requirements.txt

----------------------------------------------------
How to Run
----------------------------------------------------
1. Start the backend (FastAPI + Uvicorn):

    uvicorn src.server:app --reload

   By default, this will start the API at:
   http://127.0.0.1:8000

   You can test the API endpoints (shuffle, solve) here:
   http://127.0.0.1:8000/docs

2. Open the web interface:
   - Visit http://127.0.0.1:8000 in your browser
   - Or open static/index.html directly

----------------------------------------------------
Files
----------------------------------------------------
- src/puzzle/        : Core puzzle logic (state, search, heuristics)
- src/solve_api.py   : Solver functions called by the API
- src/server.py      : FastAPI server exposing /shuffle and /solve
- static/index.html  : Web UI for the puzzle
- requirements.txt   : Python dependencies
- README.txt         : Instructions (this file)
- Report.pdf         : Writeup about the algorithms and results

----------------------------------------------------
Extra Credit
----------------------------------------------------
- Added ability to upload a custom image and play the puzzle with it.
- Maintains API + Web integration for a smoother demo.
