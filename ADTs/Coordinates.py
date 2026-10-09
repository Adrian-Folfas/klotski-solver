class Coordinate:

    # Class should be "immutable"
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    # As for right now, only fed unit vectors, but not strictly necessary
    def get_updated_coord(self, direction_vector: tuple[int, int]) -> Coordinate:
        new_x = self.x + direction_vector[0]
        new_y = self.y + direction_vector[1]
        return Coordinate(new_x, new_y)

    def __eq__(self, other: Coordinate):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))
