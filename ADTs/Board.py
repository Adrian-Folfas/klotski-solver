from Coordinates import Coordinate

class Board:

    # exit_squares represents the Coordinates at which a hole in the wall is present,
    # which the target piece is supposed to be pushed through to end the game.
    # Bootom-left corner of the board is (0, 0)
    def __init__(self, cols: int, rows: int, exit_squares: list[Coordinate]):
        self.cols = cols
        self.rows = rows
        self.exit_squares = exit_squares
