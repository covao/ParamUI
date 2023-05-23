import numpy as np
import matplotlib.pyplot as plt
from paramui import paramui
from time import sleep

def update_board(board):
    neighbors = np.zeros(board.shape, dtype=int)
    for x_offset, y_offset in [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]:
        neighbors += np.roll(np.roll(board, y_offset, axis=1), x_offset, axis=0)
    new_board = ((neighbors == 3) | (board & (neighbors == 2))).astype(int)
    return new_board

def spawn_glider(board):
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)
    board[:3, :3] = glider
    return board

ParameterTable = [
    ['width', 'Width', 100, [10, 200, 1]],
    ['height', 'Height', 100, [10, 200, 1]],
    ['cell_size', 'Cell Size', 5, [1, 10, 1]],
    ['speed', 'Speed', 0.1, [0.01, 1, 0.01]],
    ['restart', 'Restart', False, 'button'],
    ['glider', 'Spawn Glider', False, 'button'],
]

pu = paramui(ParameterTable)
board = np.random.randint(0, 2, (pu.Prm.width, pu.Prm.height))

plt.ion()
fig, ax = plt.subplots()
img = ax.imshow(board, cmap='Greys', aspect='auto')

while plt.get_fignums():
    if pu.Prm.restart:
        board = np.random.randint(0, 2, (pu.Prm.width, pu.Prm.height))
        pu.Prm.restart = False
    if pu.Prm.glider:
        board = spawn_glider(board)
        pu.Prm.glider = False

    board = update_board(board)
    img.set_data(board)
    fig.canvas.draw()
    fig.canvas.flush_events()
    sleep(pu.Prm.speed)

plt.close(fig)
