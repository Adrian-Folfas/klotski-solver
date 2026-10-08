from Coordinates import Coordinate
from Board import Board
from Piece import Piece

class Game:

    def __init__(self, free_coords: set[Coordinate], board: Board, pieces: list[Piece]):
        self.free_coords = free_coords
        self.board = board
        self.pieces = pieces

    # Returns the piece that is trying to be moved to end of the puzzle.
    # Assumes the target piece is the largest piece in the game.
    def find_target_piece(self) -> Piece:
        return max(self.pieces, key=len)

    # Returns whether the game state represents a win or not.
    # Assumes target piece is a square
    def victory_check(self) -> bool:
        exit_squares = self.board.exit_squares
        target_piece = self.find_target_piece()
        for coord in exit_squares:
            if coord not in target_piece.coords:
                return False
        return True
