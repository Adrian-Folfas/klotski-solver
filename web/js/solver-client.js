/*
 * solver-client.js - the page's side of the conversation with the worker.
 *
 * It hides the message passing behind two things main.js can use directly:
 *
 *   solver.ready        a Promise that resolves once Python has loaded
 *   solver.solve(game)  a Promise for the solution from that position
 *
 * See solver-worker.js for the message formats.
 */

import { toSolverInput } from './model.js';

export class SolverClient {
  constructor(workerUrl) {
    this.worker = new Worker(workerUrl);

    // Solve requests waiting for an answer, keyed by request id.
    this.pending = new Map();
    this.nextId = 1;

    this.ready = new Promise((resolve, reject) => {
      this.worker.addEventListener('message', (event) => {
        const message = event.data;
        if (message.type === 'ready') {
          resolve();
        } else if (message.type === 'load-error') {
          reject(new Error(message.error));
        } else {
          this.handleAnswer(message);
        }
      });
      // Fires if the worker script itself can't be loaded or crashes.
      this.worker.addEventListener('error', (event) => {
        reject(new Error(event.message || 'The solver could not start.'));
      });
    });
  }

  /**
   * Asks the worker to solve from the given game position.
   * Resolves to the list of moves ({ cells, dir }) from bridge.py.
   */
  solve(game) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.worker.postMessage({ id, puzzle: toSolverInput(game) });
    });
  }

  handleAnswer({ id, moves, error }) {
    const request = this.pending.get(id);
    if (!request) return;
    this.pending.delete(id);
    if (error) request.reject(new Error(error));
    else request.resolve(moves);
  }
}
