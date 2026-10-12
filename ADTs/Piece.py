from .Coordinates import Coordinate
from .Board import Board

class Piece:

    def __init__(self, coords: list[Coordinate]):
        """
        Constructor for Pieces.

        Args:
            coords (list[Coordinate]): the list of Coordinates the Piece occupies.
        """
        self.coords = coords

    # Returns bool indicating whether self can be moved in given direction.
    # In practice, only fed unit vectors but should work regardless
    def can_move(self, game, direction_vector: tuple[int, int]) -> bool:
        """
        Movability checker.

        Args:
            game (Game): The current game representation
            direction_vector (tuple[int, int]): the direction vector in which to check movement.

        Return:
            bool: Whether self can move in the specified direction.
        """
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

    # Returns a new Game object representing board after a movement made.
    def move(self, game, direction_vector: tuple[int, int]):
        """
        Piece-moving function.

        Args:
            game (Game): The current game representation.
            direction_vector (tuple[int, int]): the direction vector in which to move self.

        Return:
            Game: Returns a Game object representing the game after the piece is moved.
        """
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

    def __hash__(self):
        return hash(frozenset(self.coords))
