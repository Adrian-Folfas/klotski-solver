/*
 * model.js - the game rules, in JavaScript.
 *
 * The Python ADTs are the real solver, but loading Python in the browser takes
 * a few seconds. Dragging pieces has to work instantly, so the page keeps its
 * own small copy of the movement rules here. They mirror Piece.can_move and
 * Piece.move in ADTs/Piece.py.
 *
 * A "game" in this file is a plain, immutable object:
 *
 *   {
 *     cols, rows,               board size
 *     exits:  [[x, y], ...],    exit squares
 *     pieces: [{ id, cells }],  every piece, with cells as [[x, y], ...]
 *     targetId,                 id of the piece that has to escape
 *   }
 *
 * Functions here never change a game; moving a piece returns a new game
 * (just like Piece.move returns a new Game). That makes "Back" trivial: the
 * page keeps a list of every game state and steps back through it.
 */

// The same direction vectors as DIRECTIONS in ADTs/Game.py. y grows upward,
// so [0, 1] means "up".
export const DIRECTIONS = [
  [0, 1],  // up
  [0, -1], // down
  [-1, 0], // left
  [1, 0],  // right
];

/** Builds a game from a puzzle definition (see puzzles.js). */
export function createGame(puzzle) {
  // Give every piece a stable id, so the board view can keep track of which
  // drawn block is which as they move around.
  const pieces = puzzle.pieces.map((cells, index) => ({
    id: index,
    cells: cells.map(([x, y]) => [x, y]),
  }));

  // The target is the largest piece, matching Game._find_target_piece.
  // On a tie, the first largest piece in the list wins, like Python's max().
  let target = pieces[0];
  for (const piece of pieces) {
    if (piece.cells.length > target.cells.length) target = piece;
  }

  return {
    cols: puzzle.cols,
    rows: puzzle.rows,
    exits: puzzle.exits.map(([x, y]) => [x, y]),
    pieces,
    targetId: target.id,
  };
}

/** A string key for a square, so squares can be stored in Sets and Maps. */
function squareKey(x, y) {
  return `${x},${y}`;
}

/** The set of squares covered by any piece (as squareKey strings). */
function occupiedSquares(game) {
  const occupied = new Set();
  for (const piece of game.pieces) {
    for (const [x, y] of piece.cells) occupied.add(squareKey(x, y));
  }
  return occupied;
}

export function getPiece(game, pieceId) {
  return game.pieces.find((piece) => piece.id === pieceId);
}

/**
 * Whether a piece can slide one square in a direction.
 * Mirrors Piece.can_move: every square the piece would cover must be on the
 * board, and either empty or already part of the piece itself.
 */
export function canMove(game, pieceId, [dx, dy]) {
  const piece = getPiece(game, pieceId);
  const occupied = occupiedSquares(game);
  const ownSquares = new Set(piece.cells.map(([x, y]) => squareKey(x, y)));

  return piece.cells.every(([x, y]) => {
    const nx = x + dx;
    const ny = y + dy;
    const inBounds = nx >= 0 && nx < game.cols && ny >= 0 && ny < game.rows;
    const key = squareKey(nx, ny);
    return inBounds && (!occupied.has(key) || ownSquares.has(key));
  });
}

/**
 * Returns a NEW game with one piece slid one square in a direction.
 * Assumes the move is legal (check with canMove first), like Piece.move.
 */
export function applyMove(game, pieceId, [dx, dy]) {
  return {
    ...game,
    pieces: game.pieces.map((piece) =>
      piece.id === pieceId
        ? { ...piece, cells: piece.cells.map(([x, y]) => [x + dx, y + dy]) }
        : piece,
    ),
  };
}

/** Whether the target piece covers every exit square (Game._victory_check). */
export function isSolved(game) {
  const target = getPiece(game, game.targetId);
  const targetSquares = new Set(target.cells.map(([x, y]) => squareKey(x, y)));
  return game.exits.every(([x, y]) => targetSquares.has(squareKey(x, y)));
}

/**
 * Finds the piece that covers exactly these squares, or undefined.
 * The solver describes each move by the squares the piece covers before
 * moving, and this turns that back into one of the page's pieces.
 */
export function findPieceByCells(game, cells) {
  const wanted = new Set(cells.map(([x, y]) => squareKey(x, y)));
  return game.pieces.find(
    (piece) =>
      piece.cells.length === wanted.size &&
      piece.cells.every(([x, y]) => wanted.has(squareKey(x, y))),
  );
}

/**
 * A string that identifies a position on the board.
 *
 * Like the Python game hash, it only depends on which squares each piece
 * covers, not on piece ids or list order. Two positions that look the same
 * get the same key, which is what the solution cache in main.js relies on.
 */
export function positionKey(game) {
  return game.pieces
    .map((piece) =>
      piece.cells
        .map(([x, y]) => squareKey(x, y))
        .sort()
        .join(' '),
    )
    .sort()
    .join(' | ');
}

/**
 * The plain data the Python solver needs (see web/python/bridge.py).
 * Piece ids and the target aren't sent: the solver works them out itself.
 */
export function toSolverInput(game) {
  return {
    cols: game.cols,
    rows: game.rows,
    exits: game.exits,
    pieces: game.pieces.map((piece) => piece.cells),
  };
}
