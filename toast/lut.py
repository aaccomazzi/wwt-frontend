"""
Create look-up tables to reverse-engineer
how the toast tiles are laid out

This is currently necessary because the WWT Toaster
is unscriptable. Thus, we toast the look up table,
and use that to reconstruct the proper tiles
for other images
"""
import numpy as np
from skimage.io import imsave


def lut2pos(lut):
    """Given a look up table RGB image,
    return the original positions at each pixel
    """
    r, g, b = lut[:, :, 0], lut[:, :, 1], lut[:, :, 2]
    result = g.astype(np.uint64) * 256 + r
    return result

def pos2lut(x):
    """Given a list of positions, convert to an RGB
    look up table
    """
    r = (x % 256).astype(np.uint8)
    g = (x / 256).astype(np.uint8)
    b = g * 0
    return np.dstack((r, g, b))

def main():

    y, x = np.mgrid[:1000, :2000]
    rgb = pos2lut(y)
    imsave('lut_y.png', rgb)

    rgb = pos2lut(x)
    imsave('lut_x.png', rgb)

if __name__ == "__main__":
    main()
