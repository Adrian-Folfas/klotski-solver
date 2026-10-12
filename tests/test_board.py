import unittest

from ADTs.Board import Board
from ADTs.Coordinates import Coordinate


def as_tuples(coords):
    """Converts an iterable of Coordinates to a list of (x, y) tuples, in order."""
    return [(coord.x(), coord.y()) for coord in coords]


class TestBoard(unittest.TestCase):
    """
    Testing strategy (from Testing_Partitions/board_partitions.txt):

    Partitions on cols, rows constructor inputs:
        - cols = 1, rows > 1
        - cols > 1, rows = 1
        - cols, rows both > 1

    Partitions on exit_squares constructor input:
        - Empty list
        - Some number of Coordinates

    Partitions on is_in_bounds:
        - coord is in bounds
        - coord is one step out of bounds
        - coord is far out of bounds

    "One step out of bounds" is checked off each of the four edges.
    """

    # ---------- constructor ----------

    def test_constructor_one_col_many_rows_empty_exits(self):
        # covers cols = 1, rows > 1; exit_squares empty
        board = Board(1, 5, [])
        self.assertEqual(board.cols, 1)
        self.assertEqual(board.rows, 5)
        self.assertEqual(list(board.exit_squares), [])

    def test_constructor_many_cols_one_row_with_exits(self):
        # covers cols > 1, rows = 1; exit_squares has some Coordinates
        board = Board(4, 1, [Coordinate(3, 0)])
        self.assertEqual(board.cols, 4)
        self.assertEqual(board.rows, 1)
        self.assertEqual(as_tuples(board.exit_squares), [(3, 0)])

    def test_constructor_many_cols_many_rows_with_exits(self):
        # covers cols, rows both > 1; exit_squares has some Coordinates
        board = Board(4, 5, [Coordinate(1, 0), Coordinate(2, 0)])
        self.assertEqual(board.cols, 4)
        self.assertEqual(board.rows, 5)
        self.assertEqual(as_tuples(board.exit_squares), [(1, 0), (2, 0)])

    # ---------- is_in_bounds ----------

    def test_is_in_bounds_one_col_board(self):
        # covers cols = 1, rows > 1; coord in bounds; one step out of bounds
        board = Board(1, 3, [])
        self.assertTrue(board.is_in_bounds(Coordinate(0, 0)))
        self.assertTrue(board.is_in_bounds(Coordinate(0, 2)))
        self.assertFalse(board.is_in_bounds(Coordinate(1, 0)))
        self.assertFalse(board.is_in_bounds(Coordinate(0, 3)))

    def test_is_in_bounds_one_row_board(self):
        # covers cols > 1, rows = 1; coord in bounds; one step out of bounds
        board = Board(3, 1, [])
        self.assertTrue(board.is_in_bounds(Coordinate(2, 0)))
        self.assertFalse(board.is_in_bounds(Coordinate(0, 1)))
        self.assertFalse(board.is_in_bounds(Coordinate(3, 0)))

    def test_is_in_bounds_in_bounds_corners_and_interior(self):
        # covers cols, rows both > 1; coord is in bounds
        board = Board(4, 5, [])
        for x, y in [(0, 0), (3, 0), (0, 4), (3, 4), (2, 2)]:
            with self.subTest(coord=(x, y)):
                self.assertTrue(board.is_in_bounds(Coordinate(x, y)))

    def test_is_in_bounds_one_step_out_each_edge(self):
        # covers cols, rows both > 1; coord is one step out of bounds
        board = Board(4, 5, [])
        for x, y in [(-1, 2), (4, 2), (1, -1), (1, 5)]:
            with self.subTest(coord=(x, y)):
                self.assertFalse(board.is_in_bounds(Coordinate(x, y)))

    def test_is_in_bounds_far_out(self):
        # covers cols, rows both > 1; coord is far out of bounds
        board = Board(4, 5, [])
        for x, y in [(100, 2), (1, -100), (-50, 50)]:
            with self.subTest(coord=(x, y)):
                self.assertFalse(board.is_in_bounds(Coordinate(x, y)))


if __name__ == '__main__':
    unittest.main()
