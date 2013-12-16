"""
Create toast tile directories

Usage:
python toast.py facet_to_toast
"""
import logging

import numpy as np
import healpy as hp
from toasty import toast, healpix_sampler
from PIL import Image
from urllib import urlopen
from cStringIO import StringIO

url_tmpl = 'http://cdsannotations.u-strasbg.fr/ADSAllSkySurvey/SimbadHeatMaps/healpix/%s/Norder3/Allsky.jpg'
logging.basicConfig(level=logging.INFO)


def imread(url):
    """ Read an image from a url """
    data = StringIO(urlopen(url).read())
    return np.array(Image.open(data))


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
    hps = healpix_sampler(x, nest=True)
    def lut_sampler(x, y):
        result = hps(x, y).astype(np.int)
        r = result % 256
        g = (result / 256) % 256
        b = result / 256 / 256
        np.dstack((r, g, b)).astype(np.uint8)
    toast(lut_sampler, 3, 'lut')

def harvard_sampler(all, harvard):
    hps_all = healpix_sampler(all, nest=True)
    hps_harvard = healpix_sampler(harvard, nest=True)
    def sampler(x, y):
        r = hps_harvard(x, y)
        b = hps_all(x, y)
        return np.dstack((r, b, b))
    return sampler

def run_harvard():
    url = url_tmpl % 'allSources'
    logging.info("Fetch %s",  url)
    data = np.array(imread(url))[:, :, 0]
    data = np.flipud(data)
    data = aladin_to_healpix(data)
    all = data

    url = 'http://cdsannotations.u-strasbg.fr/ADSAllSkySurvey/harvard-ads-authors/HiPS/Norder3/Allsky.jpg'
    logging.info("Fetch %s",  url)
    data = np.array(imread(url))[:, :, 0]
    data = np.flipud(data)
    data = aladin_to_healpix(data)
    harvard = data

    logging.info("Toasting harvard")
    sampler = harvard_sampler(all, harvard)
    toast(sampler, 3, 'harvard_v_all')


def run(path):
    if path == 'harvard_v_all':
        return run_harvard()

    url = url_tmpl % path.split('_512')[0]
    logging.info("Fetch %s",  url)

    data = np.array(imread(url))[:, :, 0]
    data = np.flipud(data)
    data = aladin_to_healpix(data)
    logging.info("Toasting %s", path)
    sampler = healpix_sampler(data, nest=True)
    toast(sampler, 3, path.split('.')[0])

def main():
    import sys
    map(run, sys.argv[1:])

if __name__ == "__main__":
    main()
