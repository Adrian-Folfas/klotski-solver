from ADTs.Coordinates import Coordinate
from ADTs.Piece import Piece
from ADTs.Board import Board
from ADTs.Game import Game

exit_squares = [Coordinate(1, 0), Coordinate(2, 0)]
board = Board(4, 5, exit_squares)
pieces = []

# big piece
target = Piece([Coordinate(1, 3),
                Coordinate(2, 3),
                Coordinate(1, 4),
                Coordinate(2, 4)])

#length-2
piece1 = Piece([Coordinate(0, 0),
                Coordinate(0, 1)])
piece2 = Piece([Coordinate(0, 2),
                Coordinate(0, 3)])
piece3 = Piece([Coordinate(3, 0),
                Coordinate(3, 1)])
piece4 = Piece([Coordinate(3, 2),
                Coordinate(3, 3)])
pieceside = Piece([Coordinate(1, 2),
                Coordinate(2, 2)])

#length-1
piece5 = Piece([Coordinate(1, 0)])
piece6 = Piece([Coordinate(2, 0)])
piece7 = Piece([Coordinate(1, 1)])
piece8 = Piece([Coordinate(2, 1)])

free_coords = set([Coordinate(0, 4), Coordinate(3, 4)])
pieces = [piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8, pieceside, target]
game = Game(free_coords, board, pieces)

path = game.solve_game()
for i in range(1, len(path)):
    print(i)
    print(path[i])
