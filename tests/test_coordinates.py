import unittest

from ADTs.Coordinates import Coordinate


class TestCoordinate(unittest.TestCase):
    """
    Testing strategy (from Testing_Partitions/coordinates_partitions.txt):

    Partitions on constructor inputs:
        - (0, 0)
        - Both positive integers
        - One positive, one <1
        - Both negative integers

    Partitions on x, y:
        - Called on value of 0
        - Called on non-zero value

    Partitions on get_updated_coord:
        - direction_vector = (0, 0)
        - direction vector changes only x-value
        - direction vector changes only y-value
        - direction vector changes both x, y values

    Partitions on __eq__:
        - Coordinates share no values
        - Coordinates share only x values
        - Coordinates share only y values
        - Two coordinates share both values
        - Same object in memory
    """

    # ---------- constructor, x, y ----------

    def test_constructor_origin(self):
        # covers constructor (0, 0); x, y called on value of 0
        coord = Coordinate(0, 0)
        self.assertEqual(coord.x(), 0)
        self.assertEqual(coord.y(), 0)

    def test_constructor_both_positive(self):
        # covers constructor both positive; x, y called on non-zero value
        coord = Coordinate(3, 7)
        self.assertEqual(coord.x(), 3)
        self.assertEqual(coord.y(), 7)

    def test_constructor_one_positive_one_less_than_one(self):
        # covers constructor one positive, one <1 (x positive, y negative)
        coord = Coordinate(4, -2)
        self.assertEqual(coord.x(), 4)
        self.assertEqual(coord.y(), -2)

    def test_constructor_positive_and_zero(self):
        # covers constructor one positive, one <1 (x = 0, y positive);
        #        x called on 0, y called on non-zero
        coord = Coordinate(0, 5)
        self.assertEqual(coord.x(), 0)
        self.assertEqual(coord.y(), 5)

    def test_constructor_both_negative(self):
        # covers constructor both negative; x, y called on non-zero value
        coord = Coordinate(-1, -6)
        self.assertEqual(coord.x(), -1)
        self.assertEqual(coord.y(), -6)

    # ---------- get_updated_coord ----------

    def test_get_updated_coord_zero_vector(self):
        # covers direction_vector = (0, 0)
        coord = Coordinate(2, 3)
        updated = coord.get_updated_coord((0, 0))
        self.assertEqual((updated.x(), updated.y()), (2, 3))

    def test_get_updated_coord_changes_only_x(self):
        # covers direction vector changes only x-value
        coord = Coordinate(2, 3)
        updated = coord.get_updated_coord((-1, 0))
        self.assertEqual((updated.x(), updated.y()), (1, 3))

    def test_get_updated_coord_changes_only_y(self):
        # covers direction vector changes only y-value
        coord = Coordinate(2, 3)
        updated = coord.get_updated_coord((0, 1))
        self.assertEqual((updated.x(), updated.y()), (2, 4))

    def test_get_updated_coord_changes_both(self):
        # covers direction vector changes both x, y values
        coord = Coordinate(2, 3)
        updated = coord.get_updated_coord((2, -5))
        self.assertEqual((updated.x(), updated.y()), (4, -2))

    def test_get_updated_coord_does_not_mutate_original(self):
        # covers direction vector changes both x, y values;
        # Coordinate is meant to be immutable, so the original must be unchanged
        coord = Coordinate(2, 3)
        coord.get_updated_coord((1, 1))
        self.assertEqual((coord.x(), coord.y()), (2, 3))

    # ---------- __eq__ ----------

    def test_eq_share_no_values(self):
        # covers coordinates share no values
        self.assertNotEqual(Coordinate(1, 2), Coordinate(3, 4))

    def test_eq_share_only_x(self):
        # covers coordinates share only x values
        self.assertNotEqual(Coordinate(1, 2), Coordinate(1, 4))

    def test_eq_share_only_y(self):
        # covers coordinates share only y values
        self.assertNotEqual(Coordinate(1, 2), Coordinate(3, 2))

    def test_eq_share_both_values(self):
        # covers two (distinct) coordinates share both values
        first = Coordinate(1, 2)
        second = Coordinate(1, 2)
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        self.assertEqual(second, first)

    def test_eq_same_object(self):
        # covers same object in memory
        coord = Coordinate(1, 2)
        self.assertEqual(coord, coord)


if __name__ == '__main__':
    unittest.main()
