import numpy as np
from skimage.io import imsave


def lut2pos(lut):
    r, g, b = lut[:, :, 0], lut[:, :, 1], lut[:, :, 2]
    result = g.astype(np.uint64) * 256 + r
    return result

def pos2lut(x):
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
