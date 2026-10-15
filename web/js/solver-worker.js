/*
 * solver-worker.js - runs the Python solver in a background thread.
 *
 * This is a Web Worker: it runs separately from the page, so a solve that
 * takes several seconds doesn't freeze dragging or the buttons. It:
 *
 *   1. loads Pyodide (Python compiled to WebAssembly) from a CDN,
 *   2. copies the ADTs package and web/python/bridge.py into Pyodide's
 *      virtual file system, exactly as they are in the repository,
 *   3. answers solve requests from solver-client.js.
 *
 * Messages it RECEIVES:   { id, puzzle }          puzzle as in bridge.py
 * Messages it SENDS:      { type: 'ready' }       Python is loaded
 *                         { type: 'load-error', error }
 *                         { id, moves }           a solution (see bridge.py)
 *                         { id, error }           the solve failed
 *
 * It's a "classic" (non-module) worker because Pyodide is loaded with
 * importScripts(), which module workers don't support.
 */

// Pinned so the site doesn't change behaviour when Pyodide releases a new
// version. To upgrade, change this number; the file layout on the CDN has
// stayed the same across releases.
const PYODIDE_VERSION = '0.26.4';
importScripts(`https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/pyodide.js`);

// Python files to load, as { path inside Pyodide: path relative to THIS file }.
// Paths are relative so the site works wherever it's hosted, as long as the
// repository's folder layout is kept (web/ next to ADTs/).
const PYTHON_FILES = {
  'ADTs/__init__.py': '../../ADTs/__init__.py',
  'ADTs/Coordinates.py': '../../ADTs/Coordinates.py',
  'ADTs/Board.py': '../../ADTs/Board.py',
  'ADTs/Piece.py': '../../ADTs/Piece.py',
  'ADTs/Game.py': '../../ADTs/Game.py',
  'bridge.py': '../python/bridge.py',
};

// Where the files go inside Pyodide's in-memory file system.
const PYTHON_HOME = '/home/pyodide/klotski';

// Pyodide ships an older Python than 3.14, where type hints that name a class
// inside its own body (like `-> Coordinate` in Coordinates.py) only work with
// this import at the top of the file. Adding it here means the ADTs can be
// written for Python 3.14 without breaking the website. It changes nothing
// about how the code runs.
const FUTURE_IMPORT = 'from __future__ import annotations\n';

/** Loads Pyodide and the solver. Returns the imported bridge module. */
async function loadSolver() {
  const pyodide = await loadPyodide();

  pyodide.FS.mkdirTree(`${PYTHON_HOME}/ADTs`);
  for (const [destination, source] of Object.entries(PYTHON_FILES)) {
    const url = new URL(source, self.location.href);
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Couldn't load ${url} (HTTP ${response.status})`);
    }
    const code = await response.text();
    pyodide.FS.writeFile(`${PYTHON_HOME}/${destination}`, FUTURE_IMPORT + code);
  }

  // Make `import bridge` and `import ADTs` find the files written above.
  pyodide.runPython(`import sys; sys.path.insert(0, '${PYTHON_HOME}')`);
  return pyodide.pyimport('bridge');
}

const solverReady = loadSolver();

solverReady.then(
  () => self.postMessage({ type: 'ready' }),
  (error) => self.postMessage({ type: 'load-error', error: String(error) }),
);

// Solve requests are handled one at a time, in the order they arrive.
self.onmessage = async (event) => {
  const { id, puzzle } = event.data;
  try {
    const bridge = await solverReady;
    const solutionJson = bridge.solve(JSON.stringify(puzzle));
    self.postMessage({ id, moves: JSON.parse(solutionJson) });
  } catch (error) {
    self.postMessage({ id, error: String(error) });
  }
};
