DIRECTIONS = {
    "up": (0, +1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (+1, 0),
}

pieces = []

free = {(0,4), (3,4)}

#big piece
big = {(1,3), (2,3), (1,4), (2,4)}

#length-2 pieces
piece1 = {(0,0), (0,1)}
piece2 = {(0,2), (0,3)}
piece3 = {(3,0), (3,1)}
piece4 = {(3,2), (3,3)}
pieceside = {(1,2), (2,2)}

#length-1 pieces
piece5 = {(1,0)}
piece6 = {(2,0)}
piece7 = {(1,1)}
piece8 = {(2,1)}

pieces = [piece1, piece2, piece3, piece4, piece5, piece6, piece7, piece8, pieceside, big]

board = [3,4]

game_rep = [pieces, board, free]

def victory_check(game):
    pieces = game[0]
    big = [piece for piece in pieces if len(piece) == 4]
    if (1,0) in big[0] and (2,0) in big[0]:
        return True
    return False

def try_move_piece(game, piece, dir):
    rows, cols = game[1][0], game[1][1]
    for coord in piece:
        (new_x, new_y) = (coord[0] + DIRECTIONS[dir][0], coord[1] + DIRECTIONS[dir][1])
        if not (0 <= new_x <= rows) or not (0 <= new_y <= cols):
            return None
        elif (new_x, new_y) not in game[2] and (new_x, new_y) not in piece:
            return None
        else:
            pass
    return True

def find_moves(game):
    #Return a dictionary of pieces and the moves possible for them.
    pieces = game[0]
    moves = []
    for piece in pieces:
        for dir in DIRECTIONS:
            if try_move_piece(game, piece, dir):
                moves.append((piece, dir))
    return moves

def move_piece(game, piece, dir):
    pieces, board, free = game
    free = set(free)
    dx, dy = DIRECTIONS[dir]

    new_piece_coords = set()
    for (x, y) in piece:
        new_x, new_y = x + dx, y + dy
        new_piece_coords.add((new_x, new_y))

    for coord in piece:
        free.add(coord)
    for coord in new_piece_coords:
        free.remove(coord)

    new_pieces = []
    for p in pieces:
        if p == piece:
            new_pieces.append(frozenset(new_piece_coords))
        else:
            new_pieces.append(p)
    return [new_pieces, game[1], free]


def game_hash(game):
    pieces = game[0]
    hash_set = frozenset({frozenset(piece) for piece in pieces})
    return hash(hash_set)



def bfs(game, goal_test):
    """
    Breadth-first search algorithm through games finding a path from
    the given start game to victory.

    Takes a goal test function as input to verify if end of path
    meets a specific criteria.
    """

    # Initialize queue, path, and visited set for bfs.
    queue = [(game, [])]
    visited = {game_hash(game)}
    count = 0

    # While games still exist in the queue.
    while queue:
        # Grab first game and path up to it.
        game_rep, path = queue.pop(0)
        moves = find_moves(game_rep)

        # If game state satisfies victory function, return path.
        if goal_test(game_rep) is True:
            return path

        for piece, move in moves:
            new = move_piece(game_rep, piece, move)
            # count +=1
            # print(count)
            new_hash = game_hash(new)
            if new_hash not in visited:
                visited.add(new_hash)
                queue.append((new, path + [[piece, move]]))

    # If queue is exhausted and no path is returned, then no path will exist.
    return None



def solve_klotski(game):
    return bfs(game, victory_check)

path = solve_klotski(game_rep)
i = 1
for step in path:
    print(i)
    i+=1
    print(step)
