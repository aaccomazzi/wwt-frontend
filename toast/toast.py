"""
Create toast tile directories

Usage:
python toast.py image_to_toast
"""
import os

from astropy.io import fits
import numpy as np
import healpy as hp
from healpy import ring2nest, smoothing
from toasty import toast, healpix_sampler, normalizer
from skimage.io import imread

url_tmpl = 'http://cdsannotations.u-strasbg.fr/ADSAllSkySurvey/SimbadHeatMaps/healpix/%s/Norder3/Allsky.jpg'


def natural_order(nside, ind, subn):
    assert nside <= subn
    if subn == nside:
        return np.array([ind])
    sub = hp.query_polygon(2 * nside,
                           hp.boundaries(nside, ind, nest=True).T,
                           nest=True)
    assert len(sub) == 4

    r = [natural_order(nside * 2, s, subn) for s in np.sort(sub)]
    return np.vstack((np.hstack((r[0], r[1])), np.hstack((r[2], r[3]))))


def aladin_to_healpix(data):
    """
    Convert Aladin's weird all-sky image tile to a
    respectable healpix array
    """
    inds = natural_order(8, 0, 512).ravel()
    result = np.zeros(hp.nside2npix(512), dtype=data.dtype)
    for tile in xrange(hp.nside2npix(8)):
        i, j = tile / 27, tile % 27
        sub = data[data.shape[0] - i * 64 - 64: data.shape[0] - i * 64,
                   j * 64: j * 64 + 64]
        sub = sub[::-1].T.ravel()
        result[inds + tile * 64 * 64] = sub
    return result

def make_lut():
    x = np.arange(hp.nside2npix(512))
    hp = healpix_sampler(x, nest=True)
    def lut_sampler(x, y):
        result = hp(x, y).astype(np.int)
        r = result % 256
        g = (result / 256) % 256
        b = result / 256 / 256
        np.dstack((r, g, b)).astype(np.uint8)
    toast(lut_sampler, 3, 'lut')


def run(path):
    url = url_tmpl % path.split('_512')[0]
    data = np.array(imread(url))[:, :, 0]
    data = np.flipud(data)
    data = aladin_to_healpix(data)
    sampler = healpix_sampler(data, nest=True)
    toast(sampler, 3, path.split('.')[0])


def main():
    import sys
    map(run, sys.argv[1:])

if __name__ == "__main__":
    main()
