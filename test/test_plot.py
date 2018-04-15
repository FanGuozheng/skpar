import unittest
import logging
import numpy as np
import numpy.testing as nptest
from numpy.random import random
import os
from os.path import abspath, normpath, expanduser
from numpy import pi, sqrt
from fractions import Fraction
import logging
from skpar.dftbutils.lattice import Lattice
from skpar.dftbutils.queryDFTB import get_bandstructure
from skpar.dftbutils.querykLines import get_klines, get_kvec_abscissa
from skpar.core.taskdict import plot_objvs
from skpar.dftbutils.plot import plot_bs, magic_plot_bs
np.set_printoptions(precision=2, suppress=True)

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)

def init_test_plot_bs(fn):
    """Some common initialisation for the test_plot_bs_*"""
    twd = '_workdir/test_plot'
    filename = os.path.join(twd, fn)
    if os.path.exists(fn):
        os.remove(fn)
    else:
        os.makedirs(twd, exist_ok=True)
    bsdata = np.loadtxt("reference_data/fakebands.dat", unpack=True)
    return filename, bsdata

class BandstructurePlotTest(unittest.TestCase):
    """Test bandstructure plotting back-end and magic"""

    def test_plot_bs_1(self):
        """Can we plot a bandsturcture, given as a x, and y array?"""
        filename, bsdata = init_test_plot_bs('test_plot_bs_1a.pdf')
        xx1 = bsdata[0]
        yy1 = bsdata[1:]
        xtl = None
        fig, ax = plot_bs(xx1, yy1, ylim=(-2.5, 2.5), 
                xticklabels=xtl, linelabels=['ref', 'model'],
                title='Test 1 array', xlabel=None)
        fig.savefig(filename)

    def test_plot_bs_2(self):
        """Can we plot a two bandsturctures with shared k-points?"""
        filename, bsdata = init_test_plot_bs('test_plot_bs_1b.pdf')
        xx1 = bsdata[0]
        yy1 = bsdata[1:]
        jitter = .1 * (0.5 - random(yy1.shape))
        yy2 = yy1 + jitter
        xtl = [(1, 'X'), (6, 'Gamma'), (10, 'L')]
        fig, ax = plot_bs(xx1, [yy1, yy2], ylim=(-2.5, 2.5), 
                xticklabels=xtl, linelabels=['ref', 'model'],
                title='Test 2 array common X', xlabel=None,
                filename=filename)

    def test_plot_bs_3(self):
        """Can we plot a two bandsturctures with 2 sets of k-points?"""
        filename, bsdata = init_test_plot_bs('test_plot_bs_1c.pdf')
        xx1 = bsdata[0]
        yy1 = bsdata[1:]
        jitter = .1 * (0.5 - random(yy1.shape))
        yy2 = yy1 + jitter
        xtl = [(1, 'X'), (6, 'Gamma'), (11, 'L')]
        fig, ax = plot_bs([xx1, xx1], [yy1, yy2], ylim=(-2.5, 2.5), 
                xticklabels=xtl, linelabels=['ref', 'model'],
                title='Test 2 bands 2 kpts', xlabel=None,
                filename=filename)

    def test_plot_bs_4(self):
        """Can we plot a two bandsturctures with 2 different of k-points?"""
        filename, bsdata = init_test_plot_bs('test_plot_bs_1d.pdf')
        xx1 = bsdata[0]
        yy1 = bsdata[1:]
        j = 6
        jitter = .1 * (0.5 - random(yy1[:j, :8].shape))
        yy2 = yy1[:j, :8] + jitter
        xx2 = xx1[:8]
        logger.info('yy1.shape {}, yy2.shape  {}'.format(yy1.shape, yy2.shape))
        xtl = [(1, 'X'), (6, 'Gamma'), (8, 'K'), (11, 'L')]
        fig, ax = plot_bs([xx1, xx2], [yy1, yy2], ylim=(-2.5, 2.5), 
                xticklabels=xtl, linelabels=['ref', 'model'],
                title='Test 2 bands 2 (different) kpts', xlabel=None,
                filename=filename)

class GenericPlotTaskTest(unittest.TestCase):
    """Test generic plot-task from tasksdict for  1D and 2D plots"""

    def test_plot_objvs(self):
        """Can we plot a band-structure objectives?"""
        latticeinfo = {'type': 'FCC', 'param': 5.4315}
        DB = {}
        plotname = '_workdir/test_plot/bs1.pdf'
        get_bandstructure('.', 'test_dftbutils/Si/bs/', DB,
                          latticeinfo={'type': 'FCC', 'param': 5.4315})
        bands = DB['bands']
        eps = 0.25
        jitter = eps * (0.5 - random(bands.shape))
        altbands = bands + jitter
        if os.path.exists(plotname):
            os.remove(plotname)
        else:
            os.makedirs('_workdir/test_plot', exist_ok=True)
        plot_objvs('_workdir/test_plot/bs1', DB['kvector'], [altbands, bands], 
                xticklabels=DB['kticklabels'],
                axeslabels=['wave-vector', 'Energy, eV'], 
                ylabels=['ref', 'model'], ylim=(-13, 6))
        self.assertTrue(os.path.exists(plotname))

if __name__ == '__main__':
    unittest.main()
