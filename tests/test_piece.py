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


def pieces_as_sets(game):
    """The positions of every piece in a game, independent of list order."""
    return {frozenset(as_set(piece.coords)) for piece in game.pieces}


class TestPiece(unittest.TestCase):
    """
    Testing strategy (from Testing_Partitions/piece_partitions.txt):

    partition on constructor:
        - coords has 1 coordinate
        - coords has multiple coordinates

    partition on can_move:
        - checking movement out of bounds
        - checking movement of piece into another piece
        - checking valid movement into empty square

    partition on move:
        - moving a 1x1 piece
        - moving a larger piece

    Coordinates are compared as (x, y) tuples, so these tests don't depend
    on Coordinate.__eq__ / __hash__ (those are covered in test_coordinates).
    """

    # ---------- constructor ----------

    def test_constructor_one_coordinate(self):
        # covers coords has 1 coordinate
        piece = Piece(coords_of((2, 3)))
        self.assertEqual(as_set(piece.coords), {(2, 3)})
        self.assertEqual(len(piece.coords), 1)

    def test_constructor_multiple_coordinates(self):
        # covers coords has multiple coordinates
        piece = Piece(coords_of((1, 3), (2, 3), (1, 4), (2, 4)))
        self.assertEqual(as_set(piece.coords), {(1, 3), (2, 3), (1, 4), (2, 4)})
        self.assertEqual(len(piece.coords), 4)

    # ---------- can_move ----------

    def test_can_move_out_of_bounds_single(self):
        # covers movement out of bounds; 1x1 piece
        piece = Piece(coords_of((0, 0)))
        game = Game(set(coords_of((1, 0), (0, 1), (1, 1))), Board(2, 2, []), [piece])
        self.assertFalse(piece.can_move(game, (-1, 0)))
        self.assertFalse(piece.can_move(game, (0, -1)))

    def test_can_move_out_of_bounds_larger(self):
        # covers movement out of bounds; larger piece, where only part of it
        # would leave the board
        piece = Piece(coords_of((0, 1), (0, 2)))
        game = Game(set(coords_of((0, 0))), Board(1, 3, []), [piece])
        self.assertFalse(piece.can_move(game, (0, 1)))

    def test_can_move_into_another_piece(self):
        # covers movement of piece into another piece; 1x1 pieces
        mover = Piece(coords_of((0, 0)))
        blocker = Piece(coords_of((1, 0)))
        game = Game(set(coords_of((0, 1), (1, 1))), Board(2, 2, []), [mover, blocker])
        self.assertFalse(mover.can_move(game, (1, 0)))

    def test_can_move_partially_into_another_piece(self):
        # covers movement of piece into another piece; larger piece where one
        # destination square is free and the other is occupied
        mover = Piece(coords_of((0, 0), (0, 1)))
        blocker = Piece(coords_of((1, 1)))
        game = Game(set(coords_of((1, 0))), Board(2, 2, []), [mover, blocker])
        self.assertFalse(mover.can_move(game, (1, 0)))

    def test_can_move_into_empty_square_single(self):
        # covers valid movement into empty square; 1x1 piece
        piece = Piece(coords_of((0, 0)))
        other = Piece(coords_of((1, 0)))
        game = Game(set(coords_of((0, 1), (1, 1))), Board(2, 2, []), [piece, other])
        self.assertTrue(piece.can_move(game, (0, 1)))

    def test_can_move_into_empty_square_larger(self):
        # covers valid movement into empty square; larger piece that moves
        # partly into squares it already occupies
        piece = Piece(coords_of((0, 0), (0, 1)))
        game = Game(set(coords_of((0, 2))), Board(1, 3, []), [piece])
        self.assertTrue(piece.can_move(game, (0, 1)))

    # ---------- move ----------

    def test_move_single_piece(self):
        # covers moving a 1x1 piece
        mover = Piece(coords_of((0, 0)))
        other = Piece(coords_of((1, 1)))
        game = Game(set(coords_of((1, 0), (0, 1))), Board(2, 2, []), [mover, other])

        new_game = mover.move(game, (1, 0))

        self.assertEqual(pieces_as_sets(new_game),
                         {frozenset({(1, 0)}), frozenset({(1, 1)})})
        self.assertEqual(as_set(new_game.free_coords), {(0, 0), (0, 1)})
        self.assertEqual(len(new_game.pieces), 2)

    def test_move_larger_piece(self):
        # covers moving a larger piece
        mover = Piece(coords_of((0, 0), (0, 1)))
        other = Piece(coords_of((1, 2)))
        game = Game(set(coords_of((1, 0), (1, 1), (0, 2))), Board(2, 3, []), [mover, other])

        new_game = mover.move(game, (0, 1))

        self.assertEqual(pieces_as_sets(new_game),
                         {frozenset({(0, 1), (0, 2)}), frozenset({(1, 2)})})
        self.assertEqual(as_set(new_game.free_coords), {(0, 0), (1, 0), (1, 1)})
        self.assertEqual(len(new_game.pieces), 2)

    def test_move_leaves_original_game_unchanged(self):
        # covers moving a larger piece; move returns a *new* Game, so the
        # game it was called on (and the moved piece) must not change
        mover = Piece(coords_of((0, 0), (0, 1)))
        other = Piece(coords_of((1, 2)))
        free = set(coords_of((1, 0), (1, 1), (0, 2)))
        game = Game(free, Board(2, 3, []), [mover, other])

        mover.move(game, (0, 1))

        self.assertEqual(as_set(mover.coords), {(0, 0), (0, 1)})
        self.assertEqual(pieces_as_sets(game),
                         {frozenset({(0, 0), (0, 1)}), frozenset({(1, 2)})})
        self.assertEqual(as_set(game.free_coords), {(1, 0), (1, 1), (0, 2)})


if __name__ == '__main__':
    unittest.main()
