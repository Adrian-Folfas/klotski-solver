/*
 * board-view.js - draws the board as SVG and lets the user drag pieces.
 *
 * The view never decides whether a move is allowed. When the user drags a
 * piece, it asks main.js to try one single-square step at a time (through the
 * onStep callback), and main.js calls render() again with the new game.
 *
 * Coordinates: the game uses (0, 0) as the BOTTOM-left square with y growing
 * upward, but SVG puts (0, 0) at the TOP-left with y growing downward. Every
 * conversion between the two happens in squareToSvg(), so the rest of the
 * code can think in board squares.
 */

const SVG_NS = 'http://www.w3.org/2000/svg';

// Sizes in SVG units. The SVG scales to fit its container, so these only set
// the proportions.
const CELL = 80;     // width and height of one square
const MARGIN = 12;   // space around the board, so the thick border fits
const INSET = 4;     // gap between a piece and the edge of its squares
const BORDER = 6;    // thickness of the outer wall

/** Creates an SVG element with the given attributes. */
function svgElement(tag, attributes = {}) {
  const element = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attributes)) {
    element.setAttribute(name, value);
  }
  return element;
}

/** The smallest and largest x and y covered by a piece. */
function pieceBounds(cells) {
  const xs = cells.map(([x]) => x);
  const ys = cells.map(([, y]) => y);
  return {
    minX: Math.min(...xs),
    maxX: Math.max(...xs),
    minY: Math.min(...ys),
    maxY: Math.max(...ys),
  };
}

export class BoardView {
  /**
   * @param {SVGSVGElement} svg     the <svg> element to draw into
   * @param {object}        options
   * @param {function}      options.onStep  called as onStep(pieceId, [dx, dy])
   *        when a drag wants to slide a piece one square. Should return true
   *        if the move happened (and re-render), false if it was illegal.
   */
  constructor(svg, { onStep }) {
    this.svg = svg;
    this.onStep = onStep;
    this.game = null;

    // One <g> per piece, keyed by piece id, so pieces are created once and
    // then just moved. Moving (rather than redrawing) lets CSS animate them.
    this.pieceElements = new Map();

    // Information about the drag in progress, or null.
    this.drag = null;
  }

  // ----- Drawing -----

  /** Draws the given game. The first call builds the board; later calls
   *  only move the pieces. */
  render(game) {
    const firstRender = this.game === null;
    this.game = game;

    if (firstRender) this.drawBoard();

    for (const piece of game.pieces) {
      let element = this.pieceElements.get(piece.id);
      if (!element) {
        element = this.createPieceElement(piece);
        this.pieceElements.set(piece.id, element);
      }
      // Slide the piece's group to its current squares.
      const { minX, maxY } = pieceBounds(piece.cells);
      const [left, top] = this.squareToSvg(minX, maxY);
      element.style.transform = `translate(${left}px, ${top}px)`;
    }
  }

  /** Top-left corner, in SVG units, of the square at board position (x, y). */
  squareToSvg(x, y) {
    const left = MARGIN + x * CELL;
    const top = MARGIN + (this.game.rows - 1 - y) * CELL; // flip y
    return [left, top];
  }

  /** Draws everything that never moves: grid lines and the outer wall. */
  drawBoard() {
    const { cols, rows } = this.game;
    const width = cols * CELL;
    const height = rows * CELL;
    this.svg.setAttribute('viewBox',
      `0 0 ${width + 2 * MARGIN} ${height + 2 * MARGIN}`);
    this.svg.replaceChildren();

    // Light grid lines between squares.
    const grid = svgElement('g', { class: 'grid' });
    for (let col = 1; col < cols; col++) {
      const x = MARGIN + col * CELL;
      grid.append(svgElement('line',
        { x1: x, y1: MARGIN, x2: x, y2: MARGIN + height }));
    }
    for (let row = 1; row < rows; row++) {
      const y = MARGIN + row * CELL;
      grid.append(svgElement('line',
        { x1: MARGIN, y1: y, x2: MARGIN + width, y2: y }));
    }
    this.svg.append(grid);

    this.svg.append(this.drawWalls());

    // Pieces go in their own layer, on top of the grid and walls.
    this.pieceLayer = svgElement('g', { class: 'pieces' });
    this.svg.append(this.pieceLayer);
  }

  /**
   * The thick outer wall, with a gap wherever an exit square touches the
   * edge of the board. The wall is drawn one square-edge at a time so any
   * exit, on any side, simply leaves its edge out.
   */
  drawWalls() {
    const { cols, rows, exits } = this.game;
    const isExit = (x, y) => exits.some(([ex, ey]) => ex === x && ey === y);
    const walls = svgElement('g', { class: 'walls' });

    // Adds the wall segment along one side of square (x, y), unless that
    // square is an exit. `side` is 'top', 'bottom', 'left' or 'right'.
    const addEdge = (x, y, side) => {
      if (isExit(x, y)) return;
      const [left, top] = this.squareToSvg(x, y);
      const right = left + CELL;
      const bottom = top + CELL;
      const ends = {
        top: [left, top, right, top],
        bottom: [left, bottom, right, bottom],
        left: [left, top, left, bottom],
        right: [right, top, right, bottom],
      }[side];
      const [x1, y1, x2, y2] = ends;
      walls.append(svgElement('line',
        { x1, y1, x2, y2, 'stroke-width': BORDER }));
    };

    for (let x = 0; x < cols; x++) {
      addEdge(x, rows - 1, 'top');
      addEdge(x, 0, 'bottom');
    }
    for (let y = 0; y < rows; y++) {
      addEdge(0, y, 'left');
      addEdge(cols - 1, y, 'right');
    }
    return walls;
  }

  /** Builds the SVG group for one piece. Its position is set in render(). */
  createPieceElement(piece) {
    const { minX, maxX, minY, maxY } = pieceBounds(piece.cells);
    const group = svgElement('g', { class: 'piece' });
    if (piece.id === this.game.targetId) group.classList.add('target');

    // The rectangle is drawn at the group's origin; render() moves the group.
    group.append(svgElement('rect', {
      x: INSET,
      y: INSET,
      width: (maxX - minX + 1) * CELL - 2 * INSET,
      height: (maxY - minY + 1) * CELL - 2 * INSET,
      rx: 6,
    }));

    group.addEventListener('pointerdown',
      (event) => this.startDrag(event, piece.id));
    this.pieceLayer.append(group);
    return group;
  }

  // ----- Dragging -----
  //
  // Pointer events cover mouse, touch and pen with one set of handlers.
  // While dragging, the piece follows the pointer one square at a time: each
  // time the pointer is half a square or more away from where the piece is,
  // the view tries to step the piece toward it. Every step is a real
  // single-square move, the same unit the solver uses, so the move counter
  // and the Back button treat dragged moves and solver moves the same way.

  /** Converts a pointer event's screen position into SVG units. */
  pointerToSvg(event) {
    const point = new DOMPoint(event.clientX, event.clientY);
    return point.matrixTransform(this.svg.getScreenCTM().inverse());
  }

  /** Top-left corner, in SVG units, of where a piece currently is. */
  pieceOrigin(pieceId) {
    const piece = this.game.pieces.find((p) => p.id === pieceId);
    const { minX, maxY } = pieceBounds(piece.cells);
    const [left, top] = this.squareToSvg(minX, maxY);
    return { left, top };
  }

  startDrag(event, pieceId) {
    event.preventDefault();
    const element = this.pieceElements.get(pieceId);
    // Keep receiving pointer events even if the pointer leaves the piece.
    element.setPointerCapture(event.pointerId);
    element.classList.add('dragging');

    // Remember where on the piece the user grabbed it.
    const pointer = this.pointerToSvg(event);
    const origin = this.pieceOrigin(pieceId);
    this.drag = {
      pieceId,
      element,
      grabX: pointer.x - origin.left,
      grabY: pointer.y - origin.top,
    };

    const onMove = (moveEvent) => this.continueDrag(moveEvent);
    const onEnd = () => {
      element.classList.remove('dragging');
      element.removeEventListener('pointermove', onMove);
      element.removeEventListener('pointerup', onEnd);
      element.removeEventListener('pointercancel', onEnd);
      this.drag = null;
    };
    element.addEventListener('pointermove', onMove);
    element.addEventListener('pointerup', onEnd);
    element.addEventListener('pointercancel', onEnd);
  }

  continueDrag(event) {
    if (!this.drag) return;
    const { pieceId, grabX, grabY } = this.drag;
    const pointer = this.pointerToSvg(event);

    // Step toward the pointer until the piece is as close as it can get.
    // The loop is bounded so a bug can never hang the page.
    for (let guard = 0; guard < 100; guard++) {
      const origin = this.pieceOrigin(pieceId);

      // How many whole squares the pointer is away from the piece. SVG y
      // grows downward, so it's negated to get the board's "up is +1".
      const squaresX = Math.round((pointer.x - grabX - origin.left) / CELL);
      const squaresY = -Math.round((pointer.y - grabY - origin.top) / CELL);
      if (squaresX === 0 && squaresY === 0) return;

      const stepX = [Math.sign(squaresX), 0];
      const stepY = [0, Math.sign(squaresY)];

      // Try the axis with further to go first, then the other one. Trying
      // both lets a piece slide around a corner in one drag.
      const tries = Math.abs(squaresX) >= Math.abs(squaresY)
        ? [stepX, stepY]
        : [stepY, stepX];
      const moved = tries.some(
        (step) => (step[0] !== 0 || step[1] !== 0) && this.onStep(pieceId, step),
      );
      if (!moved) return; // blocked in every useful direction
    }
  }
}
