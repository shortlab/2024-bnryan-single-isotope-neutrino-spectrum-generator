#!/usr/bin/env python
# coding: utf-8

##########################
### Imports & Variables
##########################

import sys
import numpy as np

####################################################
### Generate Electron Capture Neutrino Spectrum
####################################################

def ec_spectrum(ec_pathes) :

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