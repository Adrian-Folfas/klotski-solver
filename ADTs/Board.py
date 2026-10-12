from .Coordinates import Coordinate

class Board:

    # exit_squares represents the Coordinates at which a hole in the wall is present,
    # which the target piece is supposed to be pushed through to end the game.
    # Bootom-left corner of the board is (0, 0)
    def __init__(self, cols: int, rows: int, exit_squares: list[Coordinate]):
        """
        Constructor for Boards.

        Args:
            cols (int): number of cols, must be >0.
            rows (int): number of rows, must be >0.
            exit_squares (list): a list of Coordinates representing the exit squares.

        """
        assert cols > 0 and rows > 0, "Need >0 rows and cols!"
        self.cols = cols
        self.rows = rows
        self.exit_squares = exit_squares


    def is_in_bounds(self, coord: Coordinate) -> bool:
        """
        Returns whether the given Coordinate is in bounds on the board or not.

        Args:
            coord (Coordinate): the Coordinate to check.

        Returns:
            bool: in-bounds-ness of the coord.
        """
        return 0 <= coord.x < self.cols and 0 <= coord.y < self.rows
