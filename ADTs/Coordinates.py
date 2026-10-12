class Coordinate:

    # Class should be "immutable"
    def __init__(self, x: int, y: int):
        """
        Constructor for Coordinates.

        Args:
            x (int): x value.
            y (int): y value.
        """
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    # As for right now, only fed unit vectors, but not strictly necessary
    def get_updated_coord(self, direction_vector: tuple[int, int]) -> Coordinate:
        """
        Returns the Coordinate represented by adding self to a direction vector.

        Args:
            direction_vector (tuple[int, int]): the direction vector to add.

        Returns:
            Coordinate: the new Coordinate.
        """
        new_x = self.x() + direction_vector[0]
        new_y = self.y() + direction_vector[1]
        return Coordinate(new_x, new_y)

    def __eq__(self, other: Coordinate):
        return self._x == other.x() and self._y == other.y()

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __hash__(self):
        return hash((self._x, self._y))
