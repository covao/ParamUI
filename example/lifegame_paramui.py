"""
Conway's Game of Life visualized with ParamUI and matplotlib.
Allows interactive control of board size, seed, initial ratio, restart, and glider spawning.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from paramui import paramui

def update_board(board):
    """
    Update the board for one step of Conway's Game of Life.
    """
    neighbors = np.zeros(board.shape, dtype=int)
    # Count neighbors for each cell
    for x_offset, y_offset in [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]:
        neighbors += np.roll(np.roll(board, y_offset, axis=1), x_offset, axis=0)
    # Apply Game of Life rules
    new_board = ((neighbors == 3) | (board & (neighbors == 2))).astype(int)
    return new_board

def spawn_glider(board):
    """
    Spawn a glider at a random position on the board.
    """
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)
    rows, cols = board.shape
    gx = np.random.randint(0, rows - 2)
    gy = np.random.randint(0, cols - 2)
    board[gx:gx+3, gy:gy+3] = glider
    return board

# Parameter table for ParamUI
ParameterTable = [
    ['Size', 'Size', 100, [10, 200, 1]],
    ['Seed', 'Seed', 0, [0, 9999, 1]],
    ['InitRatio', 'Initial Ratio [%]', 50, [0, 100, 1]],
    ['Restart', 'Restart', False, 'button'],
    ['Glider', 'Spawn Glider', False, 'button'],
]

pu = paramui(ParameterTable)

def initialize_board():
    """
    Initialize the board with random cells based on parameters.
    """
    np.random.seed(int(pu.Prm.Seed))
    size = int(pu.Prm.Size)
    ratio = float(pu.Prm.InitRatio) / 100.0
    board = (np.random.rand(size, size) < ratio).astype(int)
    return board

board = initialize_board()

plt.ion()
fig, ax = plt.subplots()
img = ax.imshow(board, cmap='Greys', aspect='auto')

# Main loop: update parameters, handle buttons, and update board
while pu.IsAlive and plt.get_fignums():
    pu.update_prm()  # Update Prm Variables from UI
    if pu.Prm.Restart:
        board = initialize_board()
        pu.Prm.Restart = False
    if pu.Prm.Glider:
        board = spawn_glider(board)
        pu.Prm.Glider = False

    board = update_board(board)
    img.set_data(board)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.01)

plt.close(fig)
