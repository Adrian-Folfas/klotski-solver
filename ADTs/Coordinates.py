class Coordinate:

    # Should never be mutated
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_updated_coord(self, direction_vector: tuple[int, int]) -> Coordinate:
        new_x = self.x + direction_vector[0]
        new_y = self.y + direction_vector[1]
        return Coordinate(new_x, new_y)

    # Override == checks
    def __eq__(self, other: Coordinate):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        # h(h(x) || h(y)) shouldn't cause problems?
        return hash(int(str(hash(self.x)) +str(hash(self.y))))
