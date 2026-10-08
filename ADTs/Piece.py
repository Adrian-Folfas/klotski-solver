from .Coordinates import Coordinate
from .Board import Board

class Piece:

    def __init__(self, coords: list[Coordinate]):
        self.coords = coords

    def can_move(self, game, direction_vector: tuple[int, int]) -> bool:
        from .Game import Game
        board = game.board
        cols, rows = board.cols, board.rows
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            if not board.is_in_bounds(new_coord):
                return False
            elif new_coord not in game.free_coords and new_coord not in self.coords:
                return False
        return True

    # Returns a new Game object representing board after movement made.
    def move(self, game, direction_vector: tuple[int, int]):
        from .Game import Game
        new_coords = []
        game = game.deepcopy(skip=self)
        free_coords = game.free_coords
        for coord in self.coords:
            new_coord = coord.get_updated_coord(direction_vector)
            new_coords.append(new_coord)
            free_coords.add(coord)
        for coord in new_coords:
            free_coords.remove(coord)
        new_piece = Piece(new_coords)
        game.pieces.append(new_piece)
        return game

    # For clean printing of list of (piece, move)
    def __repr__(self):
        output = '('
        for coord in self.coords:
            output += f'{str(coord)}, '
        output += ')'
        return output
