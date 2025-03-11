#!/usr/bin/env python
# coding: utf-8

##########################
### Imports & Variables
##########################

import numpy as np

####################################################
### Generate Electron Capture Neutrino Spectrum
####################################################

def ec_spectrum(ec_pathes) :
    ''' 
    Goal: Generate the neutrino spectrum from electron capture.

    Parameters
    -----------
    ec_paths: list
              All of the decay paths that are via electron capture.

    Returns
    --------
    energies: list
              A list of the energies (in keV) that neutrinos from this isotope may have. 
    nu_spectrum: list
                 A list of the neutrino spectrum values (per keV per decay). 
    '''

    # Find Greatest Q Value
    energies = [0]
    nu_spectrum = []

    for path in ec_pathes :
        if path[0] > energies[-1] :
            energies = np.linspace(0, int(path[0]), int(path[0]) + 1)
            nu_spectrum = [0] * (int(path[0]) + 1)

    # Generate Neutrino Spectrum
    for path in ec_pathes : 
        nu_spectrum[int(path[0])] += path[1]
    
    return energies, nu_spectrum