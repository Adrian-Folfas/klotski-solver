# klotski-solver
Klotski solver I built to prove to my dad that there was a solution, even if we couldn't find it. Now iterating to build a more robust project.

Running originalexample.py prints out a sequence of numbers and lists. Numbers correspond to which move it is, and each list contains a tuple of the coordinates of a piece on the board, and a string telling you which direction to move the piece.

For coordinates, (x, y) = (col, row) with (0, 0) being the bottom-left square.

## Web frontend

The `web/` folder has a browser version that runs this solver: drag blocks, step through the shortest solution, and undo moves. See [web/README.md](web/README.md) for how to run and host it.
