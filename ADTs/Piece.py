from Coordinates import Coordinate
from Board import Board
from Game import Game

class Piece:

    def __init__(self, coords: list[Coordinate]):
        self.coords = coords

    def can_move(self, game: Game, direction_vector: tuple[int, int]) -> bool:
        board = game.board
        cols, rows = board.width, board.height
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            if not board.is_in_bounds(new_coord):
                return False
            elif new_coord not in game.free_coords and new_coord not in self.coords:
                return False
        return True

    # Returns a new Game object representing board after movement made.
    def move(self, game: Game, direction_vector: tuple[int, int]) -> Game:
        new_coords = []
        game = game.deepcopy()
        free_coords = game.free_coords
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            new_coords.append(new_coord)
            free_coords.add(coord)
        for coord in new_coords:
            free_coords.remove(coord)
        self.coords = new_coords
        return game

    # For clean printing of list of (piece, move)
    def __repr__(self):
        output = '('
        for coord in self.coords:
            output += f'{str(coord)}, '
        output += ')'
        return output
