from Coordinates import Coordinate
from Board import Board
from Piece import Piece

DIRECTIONS = {
    "up": (0, +1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (+1, 0),
}

class Game:

    def __init__(self, free_coords: set[Coordinate], board: Board, pieces: list[Piece]):
        self.free_coords = free_coords
        self.board = board
        self.pieces = pieces

        # Might use later for more efficient coord checks
        self.coords_to_pieces = {coord: piece for piece in self.pieces for coord in piece.coords}

    # Returns the piece that is trying to be moved to end of the puzzle.
    # Assumes the target piece is the largest piece in the game.
    def find_target_piece(self) -> Piece:
        return max(self.pieces, key=len)

    # Returns whether the game state represents a win or not.
    # Assumes target piece is a square
    def victory_check(self) -> bool:
        exit_squares = self.board.exit_squares
        target_piece = self.find_target_piece()
        for coord in exit_squares:
            if coord not in target_piece.coords:
                return False
        return True

    # Returns a list of tuples of (piece, legal_direction_vector)
    def find_moves(self) -> dict[Piece, tuple[int, int]]:
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

    # Hash function for game states for bfs visited checks.
    # Might need to alter in the future.
    def game_hash(self) -> int:
        hash_set = frozenset([(piece.x, piece.y) for piece in self.pieces])
        return hash(hash_set)

    def bfs(self):
        # Initialize queue, path, and visited set for bfs.
        queue = [(self, [])]
        visited = {self.game_hash()}
        count = 0

        # While games still exist in the queue.
        while queue:
            # Grab first game and path up to it.
            game, path = queue.pop(0)
            moves = self.find_moves()

            # If game state satisfies victory function, return path.
            if game.victory_check():
                return path

            for piece, direction in moves:
                new_game = piece.move(self, direction)
                new_hash = new_game.game_hash()
                if new_hash not in visited:
                    visited.add(new_hash)
                    queue.append((new_game, path + [[piece, direction]]))

        # If queue is exhausted and no path is returned, then no path will exist.
        return None

    def solve_game(self):
        return self.bfs()

    def deepcopy(self) -> Game:
        # Coords and boards are treated as immutable.
        free_coords = set(list[self.free_coords][:])
        board = self.board

        # Pieces are mutable since coordinates change, so need to reconstruct.
        pieces = [Piece([coord for piece in self.pieces for coord in piece])]
        return Game(free_coords, board, pieces)
