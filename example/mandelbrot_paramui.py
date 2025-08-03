"""
Mandelbrot set interactive visualizer using paramui and matplotlib.
Allows real-time parameter adjustment and redraw via a button.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from paramui import paramui

def mandelbrot(c, exponent, max_iter):
    """
    Calculate the number of iterations for a complex point c to escape the Mandelbrot set.
    """
    z = c
    for n in range(int(max_iter)):
        if abs(z) > 2:
            return n
        z = z ** exponent + c
    return int(max_iter)

def update_display(Prm):
    """
    Redraw the Mandelbrot set image using current parameters.
    """
    plt.clf()
    resolution = int(Prm.resolution)
    width, height = resolution, resolution  
    xmin, xmax, ymin, ymax = -2.5, 1.5, -2, 2
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    img = np.zeros((height, width))
    # Calculate Mandelbrot values for each pixel
    for i in range(height):
        for j in range(width):
            c = x[j] + 1j * y[i]
            img[i, j] = mandelbrot(c, Prm.exponent, Prm.iteration)
    plt.imshow(img, cmap=Prm.colormap, extent=(xmin, xmax, ymin, ymax))



# Parameter table for paramui
parameter_table = [
    ['exponent', 'Exponent', 2, [0.1, 10, 0.1]],
    ['iteration', 'Iteration', 10, [1, 30, 1]],
    ['colormap', 'Colormap', 'inferno',  ['inferno', 'plasma', 'viridis', 'magma']],
    ['resolution', 'Image Resolution', 200, [50, 1000, 50]], 
    ['draw', 'Draw', False, 'button'],  # add button
]

pu = paramui(parameter_table)

fig = plt.figure()
plt.ion()
plt.show()
update_display(pu.Prm)

# Main loop: update parameters and redraw when requested
while pu.IsAlive and plt.get_fignums():
    pu.update_prm()
    if pu.Prm.draw:  # draw when the draw button is pressed
        update_display(pu.Prm)
        pu.Prm.draw = False  # reset button state
        
    fig.canvas.draw()    
    fig.canvas.flush_events()

    time.sleep(0.1)

