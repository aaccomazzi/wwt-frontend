"""
Create toast tile directories

Usage:
python toast.py image_to_toast.png
"""
from skimage.io import imread, imsave
from glob import glob
from lut import lut2pos
import os
import numpy as np
from skimage.filter import median_filter

def remove_spikes(im):
    dtype = im.dtype
    lo, hi = im.min(), im.max()

    im2 = (1. * (im - lo) / (hi - lo))
    fltr = median_filter(im2, radius=2)
    diff = np.abs(1. * im2 - fltr)
    fltr = (fltr * (hi - lo) + lo).astype(dtype)

    bad = diff > max(np.median(diff) * 10, 5)
    im[bad] = fltr[bad]
    return im

def resample(x, y, im):
    x = remove_spikes(lut2pos(x))
    y = remove_spikes(lut2pos(y))
    return im[y, x]


def toast(path):
    """
    Given a path to a PNG image in cartesian projection,
    create a toast tile directory with the same name
    """
    im = imread(path)
    folder = os.path.splitext(path)[0]

    for base, dirs, files in os.walk('lut_x'):
        for file in files:
            pth = os.path.join(base, file)
            x = imread(pth)
            y = imread(pth.replace('_x', '_y'))

            out = resample(x, y, im)

            outbase = base.replace('lut_x', folder)
            if not os.path.exists(outbase):
                os.makedirs(outbase)
            pth = pth.replace('lut_x', folder)
            imsave(pth, out)


def main():
    import sys
    map(toast, sys.argv[1:])

if __name__ == "__main__":
    main()
