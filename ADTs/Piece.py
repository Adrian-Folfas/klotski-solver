from Coordinates import Coordinate
from Board import Board
from Game import Game

class Piece:

    def __init__(self, coords: list[Coordinate]):
        self.coords = coords

    def can_move(self, game: Game, direction_vector: tuple[int, int]):
        board = game.board
        cols, rows = board.width, board.height
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            if not (0 <= new_coord.x <= cols) or not (0 <= new_coord.y <= rows):
                return False
            elif new_coord not in game.free_coords and new_coord not in self.coords:
                return False
        return True

    def move(self, game: Game, direction_vector: tuple[int, int]):
        new_coords = []
        free_coords = game.free_coords
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            new_coords.append(new_coord)
            free_coords.add(coord)
        for coord in new_coords:
            free_coords.remove(coord)
        return game
