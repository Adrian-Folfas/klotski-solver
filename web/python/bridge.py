"""
Bridge between the web frontend and the Python solver in ADTs/.

The browser runs this file (together with the ADTs package) inside Pyodide,
a version of Python compiled to WebAssembly. JavaScript and Python only
exchange plain JSON strings through it, so the ADTs never need to know they
are running on a web page.

Puzzle JSON (sent by the page, built in web/js/model.js -> toSolverInput):
    {
        "cols": 4,
        "rows": 5,
        "exits": [[1, 0], [2, 0]],
        "pieces": [[[1, 3], [2, 3], [1, 4], [2, 4]], [[0, 0], [0, 1]], ...]
    }
    Every square is an [x, y] pair, with (0, 0) the bottom-left square,
    exactly like the Coordinates used by the ADTs.

Solution JSON (sent back to the page):
    [{"cells": [[0, 2], [0, 3]], "dir": [0, 1]}, ...]
    One entry per single-square move, in order. "cells" are the squares the
    piece occupies *before* the move, which is how the page finds the piece.
    An empty list means either "already solved" or "no solution exists";
    the page can tell those apart itself.
"""

import json

from ADTs.Board import Board
from ADTs.Coordinates import Coordinate
from ADTs.Game import Game
from ADTs.Piece import Piece


def build_game(puzzle: dict) -> Game:
    """
    Builds a Game from a decoded puzzle dictionary (see the module docstring).

    Free squares aren't sent by the page: they are every square on the board
    that no piece covers.
    """
    cols, rows = puzzle["cols"], puzzle["rows"]

    pieces = [Piece([Coordinate(x, y) for x, y in cells]) for cells in puzzle["pieces"]]

    occupied = {(x, y) for cells in puzzle["pieces"] for x, y in cells}
    free_coords = {Coordinate(x, y)
                   for x in range(cols)
                   for y in range(rows)
                   if (x, y) not in occupied}

    board = Board(cols, rows, [Coordinate(x, y) for x, y in puzzle["exits"]])
    return Game(free_coords, board, pieces)


def solve(puzzle_json: str) -> str:
    """
    Solves a puzzle given as a JSON string and returns its solution as a JSON
    string (formats described in the module docstring).
    """
    game = build_game(json.loads(puzzle_json))
    path = game.solve_game()

    moves = [
        {
            "cells": [[coord.x(), coord.y()] for coord in piece.coords],
            "dir": [direction[0], direction[1]],
        }
        for piece, direction in path
    ]
    return json.dumps(moves)
