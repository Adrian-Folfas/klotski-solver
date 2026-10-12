import unittest

from ADTs.Board import Board
from ADTs.Coordinates import Coordinate
from ADTs.Game import Game
from ADTs.Piece import Piece


def coords_of(*pairs):
    """Builds a list of Coordinates from (x, y) pairs."""
    return [Coordinate(x, y) for x, y in pairs]


def as_set(coords):
    """Converts an iterable of Coordinates to a set of (x, y) tuples."""
    return {(coord.x(), coord.y()) for coord in coords}


def make_game(cols, rows, exits, pieces):
    """
    Builds a Game from plain (x, y) tuples.

    Args:
        cols, rows (int): board dimensions.
        exits (list[tuple[int, int]]): exit squares.
        pieces (list[list[tuple[int, int]]]): one list of squares per piece.
    """
    occupied = {square for piece in pieces for square in piece}
    free = {(x, y) for x in range(cols) for y in range(rows)} - occupied
    return Game(set(coords_of(*free)),
                Board(cols, rows, coords_of(*exits)),
                [Piece(coords_of(*piece)) for piece in pieces])


class TestSolveGame(unittest.TestCase):
    """
    Testing strategy (from Testing_Partitions/game_partitions.txt):

    partition on solve_game:
        - unsolvable game
        - solvable game

    For solvable games, rather than comparing against one hard-coded path
    (several shortest paths can exist), each returned move is replayed
    through Piece.can_move / Piece.move to check it is legal, and the final
    position is checked to have the target piece covering every exit square.
    Since solve_game is a BFS, path lengths are also checked to be minimal.
    """

    def assert_valid_solution(self, game, path):
        """Replays path from game; fails unless every move is legal and the
        final position is a win. The target is the largest piece."""
        target_size = max(len(piece.coords) for piece in game.pieces)
        exits = as_set(game.board.exit_squares)

        for step, (piece, direction) in enumerate(path, start=1):
            squares = as_set(piece.coords)
            matches = [p for p in game.pieces if as_set(p.coords) == squares]
            self.assertEqual(len(matches), 1,
                             f"move {step}: no piece at {sorted(squares)}")
            current = matches[0]
            self.assertTrue(current.can_move(game, direction),
                            f"move {step}: illegal move {direction} for {sorted(squares)}")
            game = current.move(game, direction)

        target = [p for p in game.pieces if len(p.coords) == target_size][0]
        self.assertTrue(exits <= as_set(target.coords),
                        "final position does not have the target on the exit")

    # ---------- unsolvable ----------

    def test_unsolvable_no_legal_moves(self):
        # covers unsolvable game; board is full, so no piece can move at all
        game = make_game(2, 2, [(0, 0), (1, 0)],
                         [[(0, 1), (1, 1)],   # target
                          [(0, 0)],
                          [(1, 0)]])
        self.assertEqual(game.solve_game(), [])

    def test_unsolvable_with_legal_moves(self):
        # covers unsolvable game; pieces can move, but the full-width target
        # can never get past the blocker below it, so every reachable state
        # must be explored before giving up
        game = make_game(2, 3, [(0, 0), (1, 0)],
                         [[(0, 2), (1, 2)],   # target
                          [(0, 0)]])          # blocker
        self.assertEqual(game.solve_game(), [])

    # ---------- solvable ----------

    def test_solvable_single_piece(self):
        # covers solvable game; only the target, which slides straight down
        game = make_game(1, 3, [(0, 0)],
                         [[(0, 2)]])
        path = game.solve_game()
        self.assertEqual(len(path), 2)
        self.assert_valid_solution(game, path)

    def test_solvable_blocker_must_move_first(self):
        # covers solvable game; the blocker has to move out of the target's
        # column (2 moves) before the target can slide down (2 moves)
        game = make_game(3, 3, [(0, 0), (1, 0)],
                         [[(0, 2), (1, 2)],   # target
                          [(0, 0)]])          # blocker
        path = game.solve_game()
        self.assertEqual(len(path), 4)
        self.assert_valid_solution(game, path)

    def test_solvable_classic_layout(self):
        # covers solvable game; the full layout from originalexample.py,
        # whose shortest solution is 114 single-square moves
        game = make_game(4, 5, [(1, 0), (2, 0)],
                         [[(1, 3), (2, 3), (1, 4), (2, 4)],   # target
                          [(0, 0), (0, 1)],
                          [(0, 2), (0, 3)],
                          [(3, 0), (3, 1)],
                          [(3, 2), (3, 3)],
                          [(1, 2), (2, 2)],
                          [(1, 0)],
                          [(2, 0)],
                          [(1, 1)],
                          [(2, 1)]])
        path = game.solve_game()
        self.assertEqual(len(path), 114)
        self.assert_valid_solution(game, path)


if __name__ == '__main__':
    unittest.main()
