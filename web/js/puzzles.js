/*
 * puzzles.js - puzzle definitions.
 *
 * A puzzle is plain data, so a new layout (or a different board size) is just
 * another object in this shape. Nothing else in the frontend hard-codes the
 * board size or the pieces.
 *
 *   {
 *     name:   shown in the page's heading,
 *     cols:   board width in squares,
 *     rows:   board height in squares,
 *     exits:  squares the target piece must cover to win, as [x, y] pairs,
 *     pieces: one list of [x, y] squares per piece,
 *   }
 *
 * Coordinates match the Python ADTs: x is the column, y is the row, and
 * (0, 0) is the BOTTOM-left square (y grows upward).
 *
 * The target piece is not marked here. Like Game._find_target_piece in
 * ADTs/Game.py, the frontend treats the largest piece as the target, so the
 * page and the solver always agree on which piece has to escape.
 *
 * Pieces are drawn as rectangles (see pieceBounds in board-view.js), which
 * fits every Klotski piece. Each piece's squares must form a filled rectangle.
 */

// The layout from originalexample.py.
export const CLASSIC = {
  name: 'Klotski',
  cols: 4,
  rows: 5,
  exits: [[1, 0], [2, 0]],
  pieces: [
    // The 2x2 target block, top middle.
    [[1, 3], [2, 3], [1, 4], [2, 4]],

    // Four vertical 1x2 blocks along the sides.
    [[0, 0], [0, 1]],
    [[0, 2], [0, 3]],
    [[3, 0], [3, 1]],
    [[3, 2], [3, 3]],

    // One horizontal 2x1 block under the target.
    [[1, 2], [2, 2]],

    // Four 1x1 blocks at the bottom middle.
    [[1, 0]],
    [[2, 0]],
    [[1, 1]],
    [[2, 1]],
  ],
};
