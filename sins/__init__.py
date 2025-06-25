"""
SINS (Single Isotope Neutrino Spectrum generator)

A python pacakged designed to create neutrino spectra for 
the radioactive decay of any isotope.
"""

__version__ = "0.1.0"
__author__ = 'Brianna Noelani Ryan'
__credits__ = 'MIT Laboratory of Nuclear Science'

from .sins import generate
from .sins import plot
from .sins import make_csv