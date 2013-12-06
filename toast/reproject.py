"""
Convert healpix maps into cartesian projection maps suitable
for toasting

Usage:
python reproject.py healpix_path_without_suffix
"""
from glob import glob
from astropy.io import fits
from healpy.projector import CartesianProj
from healpy import vec2pix, smoothing, nest2ring, ring2nest
import numpy as np
from matplotlib.colors import LogNorm
from skimage.io import imsave
from glue.clients.ds9norm import DS9Normalize

NSIDE=512
WIDTH=2600

v2p = lambda x, y, z: vec2pix(NSIDE, x, y, z, nest=False)

def make_map(m):
    p = CartesianProj(xsize=WIDTH)
    result = p.projmap(m, v2p)
    print result.shape
    return result

def normalize(im):
    norm = DS9Normalize()
    norm.vmin = im.min()
    norm.vmax = max(norm.vmin * 1.05, im.max())
    norm.bias = .2
    norm.contrast = 2
    norm.stretch = 'log'
    result = norm(im.astype(np.float)) * 255
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result

def smooth_map(im):
    ind = np.arange(im.size)
    ind = ring2nest(NSIDE, ind)
    im = im[ind]
    result =  smoothing(im, fwhm = np.radians(.3))
    return result


def build_image(m):
    result = smooth_map(m)
    result = make_map(result)
    result = normalize(result)
    result = np.flipud(result)
    return result

def runner(files=None):
    files = files or glob('*hpx')
    for file in files:
        m = fits.open(file)[1].data['density512']
        m = build_image(m)
        outfile = file.replace('.hpx', '.png')
        imsave(outfile, m)

def main():
    import sys
    files = [x + '.hpx' for x in sys.argv[1:]]
    runner(files)

if __name__ == "__main__":
    main()
