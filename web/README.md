# Web frontend

A browser version of the solver. You can drag blocks around, step forward
through the shortest solution with **Next**, undo moves with **Back**, and see
how many moves have been made.

The page runs the real Python solver from `ADTs/` inside the browser, using
[Pyodide](https://pyodide.org) (Python compiled to WebAssembly). There is no
server-side code, so the site can be hosted anywhere that serves static files.

## Running it locally

Browsers won't load JavaScript modules or the Python files from a `file://`
URL, so serve the repository with any static web server. From the
**repository root** (not from `web/`):

```
python3 -m http.server 8000
```

Then open <http://localhost:8000/web/>.

The first visit downloads Pyodide (roughly 10 MB) from the jsDelivr CDN, so
"Next" takes a few seconds to become available. Dragging works straight away.

## Hosting

Upload the repository as-is to any static host (GitHub Pages, Netlify, your
own site) and visit `/web/`. The only requirement is to keep `web/` and
`ADTs/` side by side, because the page loads the solver's Python files from
`../ADTs/`.

For GitHub Pages: Settings → Pages → deploy from the `main` branch, root
folder. The page is then at `https://<user>.github.io/klotski-solver/web/`.

## How the code is organised

| File | What it does |
|---|---|
| `index.html` | Page structure: board, message box, buttons, move counter. |
| `style.css` | All styling. Colours are variables at the top. |
| `js/puzzles.js` | Puzzle definitions as plain data. |
| `js/model.js` | The game rules in JavaScript (mirrors `Piece.can_move` / `Piece.move`), so dragging works without waiting for Python. |
| `js/board-view.js` | Draws the board as SVG and turns drags into single-square moves. |
| `js/main.js` | Connects everything: move history, Next/Back, the counter, the status message, and caching solutions. |
| `js/solver-client.js` | The page's side of talking to the solver worker. |
| `js/solver-worker.js` | Background thread that loads Pyodide and the Python files and runs solves, so the page never freezes. |
| `python/bridge.py` | Converts between the page's JSON and the ADTs, and calls `Game.solve_game`. |

Data flows like this:

```
puzzles.js ──▶ model.js (game state) ──▶ board-view.js (SVG, dragging)
                    │
                    └─▶ solver-client.js ──▶ solver-worker.js ──▶ bridge.py ──▶ ADTs/
```

## Things to know when changing it

- **Coordinates** are the same as in the ADTs: `(x, y)` = `(column, row)`,
  with `(0, 0)` the bottom-left square. Only `squareToSvg()` in
  `board-view.js` flips y for drawing.
- **The target piece** is the largest piece, worked out the same way as
  `Game._find_target_piece`. If that rule changes in Python, change
  `createGame()` in `model.js` too.
- **Movement rules exist twice**: in Python (for solving) and in `model.js`
  (for dragging). If you change what counts as a legal move, update both.
- **Pieces are drawn as rectangles** from the squares they cover
  (`pieceBounds()` in `board-view.js`). Non-rectangular pieces would need a
  different drawing function.
- **Pyodide runs an older Python than 3.14.** The worker adds
  `from __future__ import annotations` to the top of each Python file it
  loads, so type hints like `-> Coordinate` inside the `Coordinate` class
  keep working. The Pyodide version is pinned in `js/solver-worker.js`.

## Adding your own puzzle layouts

A puzzle is just data (see the comment at the top of `js/puzzles.js`), and
nothing else in the frontend assumes the classic 4×5 layout. Board size,
walls, exits and pieces all come from the puzzle object. To show a different
puzzle, give `PUZZLE` in `js/main.js` another object in the same format.
