import numpy as np
import matplotlib.pyplot as plt
from paramui import paramui

def mandelbrot(c, exponent, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z ** exponent + c
    return max_iter

def mandelbrot_set(exponent, max_iter, image_size, colormap):
    width, height = image_size
    xmin, xmax, ymin, ymax = -2.5, 1.5, -2, 2
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    img = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            c = x[j] + 1j * y[i]
            img[i, j] = mandelbrot(c, exponent, max_iter)

    plt.imshow(img, cmap=colormap, extent=(xmin, xmax, ymin, ymax))
    plt.pause(0.1)
    plt.show()

def update_display(Prm):
    plt.clf()
    mandelbrot_set(Prm.exponent, Prm.iteration, (Prm.width, Prm.height), Prm.colormap)

parameter_table = [
    ['exponent', 'Exponent', 2, [0.1, 10, 0.1]],
    ['iteration', 'Iteration', 10, [1, 100, 1]],
    ['colormap', 'Colormap', 'inferno',  ['inferno', 'plasma', 'viridis', 'magma']],
    ['width', 'Image Width', 200, [100, 1000, 100]],
    ['height', 'Image Height', 200, [100, 1000, 100]],
]

paramui(parameter_table, update_display)

