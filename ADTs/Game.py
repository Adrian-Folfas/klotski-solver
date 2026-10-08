from Coordinates import Coordinate
from Board import Board
from Piece import Piece

class Game:

    def __init__(self, free_coords: set[Coordinate], board: Board, pieces: list[Piece]):
        self.free_coords = free_coords
        self.board = board
        self.pieces = pieces
