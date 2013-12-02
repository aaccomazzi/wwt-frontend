from skimage.io import imread, imsave
from glob import glob
from lut import lut2pos
import os

def resample(x, y, im):
    x = lut2pos(x)
    y = lut2pos(y)
    return im[y, x]


def toast(path):
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
