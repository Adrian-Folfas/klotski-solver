from .Coordinates import Coordinate
from .Board import Board
from .Piece import Piece

DIRECTIONS = [
    (0, +1),
    (0, -1),
    (-1, 0),
    (+1, 0)
]

class Game:

    def __init__(self, free_coords: set[Coordinate], board: Board, pieces: list[Piece]):
        """
        Constructor for Games.

        Args:
            free_coord (set[Coordinate]): The set of unoccupied Coordinates.
            board (Board): The game board.
            pieces (list[Piece]): The pieces on the board.
        """
        self.free_coords = free_coords
        self.board = board
        self.pieces = pieces

        # Might use later for more efficient coord checks
        # self.coords_to_pieces = {coord: piece for piece in self.pieces for coord in piece.coords}

    def find_target_piece(self) -> Piece:
        """
        Finds the piece we're trying to free.

        Return:
            Piece: The largest Piece on the board.
        """
        return max(self.pieces, key=lambda p: len(p.coords))

    def victory_check(self) -> bool:
        """
        Victory checker.

        Return:
            bool: Whether the game has been won.
            Assumes that exit dimensions align with target piece dimensions
        """
        exit_squares = self.board.exit_squares
        target_piece = self.find_target_piece()
        for coord in exit_squares:
            if coord not in target_piece.coords:
                return False
        return True

    def find_moves(self) -> list[Piece, tuple[int, int]]:
        """
        Legal move finder for game representation.

        Return:
           list[Piece, tuple[int, int]]: A list of tuples containing pieces
                                         and the directions they can move in.
        """
        moves = []
        for piece in self.pieces:
            for direction_vector in DIRECTIONS:
                if piece.can_move(self, direction_vector):
                    moves.append((piece, direction_vector))
        return moves

    # Maybe for a future optimized version?
    #
    # def find_moves(self) -> dict[Piece, tuple[int, int]]:
    #     output = {}
    #     for free_coord in self.free_coords:
    #         for direction_vector in DIRECTIONS:
    #             new_coord = Coordinate(free_coord.x + direction_vector[0],
    #                                    free_coord.y + direction_vector[1])
    #             if not self.board.is_in_bounds(new_coord) or new_coord in self.free_coords:
    #                 continue
    #             else:

    def game_hash(self) -> int:
        """
        Hash for game states.

        Return:
            int: a hopefully-unique identifier for a game state.
        """
        return hash(frozenset([piece for piece in self.pieces]))

    def bfs(self):
        """
        BFS on legal moves to solve game.

        Return:
            Empty list if no solution exists, otherwise a list of lists, where each sub-list
            contains the piece and direction vector it should be moved, in puzzle-solving order.
        """
        # Initialize queue, path, and visited set for bfs.
        queue = [(self, [])]
        visited = {self.game_hash()}

        # While games still exist in the queue.
        while queue:
            # Grab first game and path up to it.
            game, path = queue.pop(0)
            moves = game.find_moves()
            # If game state satisfies victory function, return path.
            if game.victory_check():
                return path

            for piece, direction in moves:
                new_game = piece.move(game, direction)
                new_hash = new_game.game_hash()
                if new_hash not in visited:
                    visited.add(new_hash)
                    queue.append((new_game, path + [[piece, direction]]))

        # If queue is exhausted and no path is returned, then no path will exist.
        return []

    def solve_game(self):
        """
        Game solver.

        Return:
            Empty list if no solution exists, otherwise a list of lists, where each sub-list
            contains the piece and direction vector it should be moved, in puzzle-solving order.
        """
        return self.bfs()

    # Optional parameter to avoid copying over a specific piece.
    def deepcopy(self, skip=None) -> Game:
        """
        Method to return a second Game object representing the same state,
        potentially with the exception of one piece.

        Args:
            skip (Piece | None): A Piece to not copy, or None if full-copy required.

        Return:
            Game: A new Game object of the same state, with the exception of the possibly specified
                  uncopied piece.
        """
        # Coords and boards are treated as immutable.
        free_coords = set(list(self.free_coords)[:])
        board = self.board

        # Pieces are mutable since coordinates change, so need to reconstruct.
        pieces = []
        for piece in self.pieces:
            if piece is skip:
                continue
            coords = []
            for coord in piece.coords:
                coords.append(coord)
            new_piece = Piece(coords)
            pieces.append(new_piece)

        return Game(free_coords, board, pieces)
