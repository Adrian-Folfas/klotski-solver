/*
 * main.js - connects the board, the buttons, the move counter and the solver.
 *
 * How the controls behave:
 *
 *   - Dragging a block slides it one square at a time. Each square counts as
 *     one move, the same unit the solver uses.
 *   - "Back" undoes the most recent move, whether you dragged it or "Next"
 *     made it.
 *   - "Next" plays one move of the shortest solution from the CURRENT
 *     position. If you've moved blocks yourself, the solver works out a new
 *     shortest solution from wherever the board is now.
 *   - The move counter shows how many moves have been made from the start.
 *
 * Solutions are cached by position, so stepping through a solution only
 * calls the solver once.
 */

import { CLASSIC } from './puzzles.js';
import {
  applyMove,
  canMove,
  createGame,
  findPieceByCells,
  isSolved,
  positionKey,
} from './model.js';
import { BoardView } from './board-view.js';
import { SolverClient } from './solver-client.js';

// The puzzle to show. Any puzzle in the format described in puzzles.js
// works here, including other board sizes.
const PUZZLE = CLASSIC;

// ----- Page elements -----

const titleElement = document.querySelector('#title');
const statusElement = document.querySelector('#status');
const backButton = document.querySelector('#back');
const nextButton = document.querySelector('#next');
const counterElement = document.querySelector('#move-counter');

// ----- State -----

// Every position since the start, oldest first. The last one is on screen,
// and its index is the number of moves made. "Back" just drops the last one.
const history = [createGame(PUZZLE)];

// Solutions we already know, as positionKey -> remaining moves from there.
// An empty list means the position is solved; null means it has no solution.
const solutionCache = new Map();

// Solves that are running, as positionKey -> Promise, so the same position
// is never sent to the solver twice at once.
const runningSolves = new Map();

// 'loading' until Python is ready, then 'ready', or 'failed'.
let solverState = 'loading';

const currentGame = () => history[history.length - 1];
const movesMade = () => history.length - 1;

// ----- Solver -----

const solver = new SolverClient(new URL('./solver-worker.js', import.meta.url));

/**
 * Stores a solution in the cache. Besides the starting position, every
 * position along the solution gets an entry too (with the rest of the
 * moves), which is what makes repeated "Next" presses instant.
 */
function cacheSolution(game, moves) {
  if (moves.length === 0) {
    // The solver returns [] both for "already solved" and "no solution".
    solutionCache.set(positionKey(game), isSolved(game) ? [] : null);
    return;
  }
  let position = game;
  moves.forEach((move, index) => {
    solutionCache.set(positionKey(position), moves.slice(index));
    const piece = findPieceByCells(position, move.cells);
    position = applyMove(position, piece.id, move.dir);
  });
  solutionCache.set(positionKey(position), []);
}

/** Makes sure the solution from this position is in the cache. */
function solveFrom(game) {
  const key = positionKey(game);
  if (solutionCache.has(key)) return Promise.resolve();
  if (!runningSolves.has(key)) {
    const request = solver
      .solve(game)
      .then((moves) => cacheSolution(game, moves))
      .finally(() => {
        runningSolves.delete(key);
        updateControls();
      });
    runningSolves.set(key, request);
  }
  return runningSolves.get(key);
}

// ----- Moves -----

/** Puts a new position on screen and records it in the history. */
function pushGame(game) {
  history.push(game);
  board.render(game);
  updateControls();
}

/** Called by the board while dragging: tries to slide a piece one square. */
function tryStep(pieceId, direction) {
  const game = currentGame();
  if (!canMove(game, pieceId, direction)) return false;
  pushGame(applyMove(game, pieceId, direction));
  return true;
}

function stepBack() {
  if (history.length <= 1) return;
  history.pop();
  board.render(currentGame());
  updateControls();
}

async function stepForward() {
  const game = currentGame();
  const key = positionKey(game);
  if (isSolved(game)) return;

  if (!solutionCache.has(key)) {
    try {
      await solveFrom(game);
    } catch (error) {
      console.error(error);
      statusElement.textContent = `The solver hit an error: ${error.message}`;
      return;
    }
    // If blocks were dragged while the solver was thinking, the answer is
    // for a position that's no longer on screen, so don't apply it.
    if (positionKey(currentGame()) !== key) return;
  }

  const moves = solutionCache.get(key);
  if (!moves || moves.length === 0) return; // unsolvable (status says so)

  const [nextMove] = moves;
  const piece = findPieceByCells(game, nextMove.cells);
  pushGame(applyMove(game, piece.id, nextMove.dir));
}

// ----- Buttons, counter and status message -----

/** Brings the buttons, counter and status text up to date. */
function updateControls() {
  const game = currentGame();
  const key = positionKey(game);
  const solved = isSolved(game);
  const solving = runningSolves.has(key);
  const known = solutionCache.get(key); // undefined if not solved yet

  counterElement.textContent = `Moves: ${movesMade()}`;
  backButton.disabled = history.length <= 1;
  nextButton.disabled =
    solved || solving || solverState !== 'ready' || known === null;

  if (solved) {
    statusElement.textContent =
      `Solved! The red block reached the exit in ${movesMade()} moves.`;
  } else if (solverState === 'loading') {
    statusElement.textContent =
      'Loading the solver... You can already drag blocks.';
  } else if (solverState === 'failed') {
    statusElement.textContent =
      'The solver could not load, so Next is unavailable. Dragging still works.';
  } else if (solving) {
    statusElement.textContent = 'Finding the shortest solution from here...';
  } else if (known === null) {
    statusElement.textContent = 'There is no solution from this position.';
  } else if (known) {
    statusElement.textContent =
      `Shortest solution from here: ${known.length} moves.`;
  } else {
    statusElement.textContent = 'Press Next to see the best move from here.';
  }
}

// ----- Start up -----

titleElement.textContent = PUZZLE.name;

const board = new BoardView(document.querySelector('#board'), {
  onStep: tryStep,
});
board.render(currentGame());

backButton.addEventListener('click', stepBack);
nextButton.addEventListener('click', stepForward);
updateControls();

solver.ready.then(
  () => {
    solverState = 'ready';
    updateControls();
    // Solve the current position straight away, so the first "Next" press
    // (and the "moves left" count) don't have to wait.
    solveFrom(currentGame()).catch((error) => console.error(error));
    updateControls();
  },
  (error) => {
    console.error(error);
    solverState = 'failed';
    updateControls();
  },
);
