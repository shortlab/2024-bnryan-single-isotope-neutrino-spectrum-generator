# __main__.py
#!/usr/bin/env python
# coding: utf-8

##########################
### Imports & Variables
##########################

import sys
import csv
import matplotlib.pyplot as plt

from beta import beta_decay_spectrum
from ec import ec_spectrum 

##########################
### Getting Inputs
##########################

### Read Data File
def read_file(file_name) :
    ''' 
    Goal: Read the provided csv file of the decay pathes of an isotope.

    Parameters
    -----------
    file_name: str
               The name of the csv file containing the starting isotope and it's decay paths.

    Returns
    --------
    start_iso: tuple 
               The information about the initial isotope. Follows the format (Decay Type, Isotope, Z, A, Spin, Parity, Q, Branching Ratio)
    beta_pathes: list
                 This list contains the tuples of information for the beta decay pathes of the starting isotope
    ec_pathes: list
               This list contains the tuples of information for the electron capture decay pathes of the starting isotope
    '''
    with open(file_name) as file :
        reader = csv.reader(file)
        header = next(reader)

        beta_pathes = []
        ec_pathes = []

        for row in reader :
            if row[0] == 'Start' :
                start_iso = (row[1], int(row[2]), int(row[3]), float(row[4]), int(row[5]), float(row[6]), float(row[7]))
            if row[0] == 'Beta' :
                beta_pathes.append((row[1], int(row[2]), int(row[3]), float(row[4]), int(row[5]), float(row[6]), float(row[7])))
            if row[0] == 'EC' :
                ec_pathes.append((float(row[6]), float(row[7])))

    return start_iso, beta_pathes, ec_pathes

###################
### Saving Data
###################

def plot(energy, spectrum, particle, iso_name) :
    ''' 
    Goal: Plot Spectra

    Parameters
    -----------
    energy: list
            The energies associated with the provided spectra.
    spectrum: list
              The number of particle per keV per decay.
    particle: str
              The particle being shown in the spectrum.
    iso_name: str
              Name of the isotope of interest.
    '''

    plt.plot(energy, spectrum, color='black')
    plt.ylabel('dN/dE (' + particle + 's/keV/Decay)')
    plt.xlabel(particle + ' Energy (keV)')
    plt.title(iso_name + ' ' + particle + ' Spectrum')
    plt.savefig(iso_name + '_' + particle + '_Spectrum.png')
    plt.show()

def make_csv(energy, spectrum, particle, iso_name) :
    ''' 
    Goal: Generate csv file with the given spectrum data.

    Parameters
    -----------
    energy: list
            The energies associated with the provided spectra.
    spectrum: list
              The number of particle per keV per decay.
    particle: str
              The particle being shown in the spectrum.
    iso_name: str
              Name of the isotope of interest.
    '''

    csv_file = iso_name + '_' + particle + '_Spectrum.csv'

    with open(csv_file, 'w', newline='') as file:
        fieldnames = ['energy', 'dN/dE']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(energy)) :
            writer.writerow({'energy': energy[i], 'dN/dE': spectrum[i]})

##########################
### Main Function
##########################

if __name__ == '__main__':

    # Define Input Variables
    file_name = sys.argv[1]

    # Read Input File
    start, beta_pathes, ec_pathes = read_file(file_name)
    print(beta_pathes)
    # Generate Each Decay Pathes Neutrino Spectrum
    if beta_pathes != [] :
        beta_energies, beta_beta, beta_nu = beta_decay_spectrum(start, beta_pathes)
    if ec_pathes != [] :
        ec_energies, ec_nu = ec_spectrum(ec_pathes)

    # Define Complete Spectrum
    energy = []
    spectrum = []

    # if there is only beta decay
    if beta_pathes == [] :
        energy = list(ec_energies)
        spectrum = ec_nu

        # stretching beyond the peak to properly show it
        for i in range(int(energy[-1]/10)) :
            energy.append(energy[-1] + 1)
            spectrum.append(0)
    
    # if there is only electron capture
    elif ec_pathes == [] :
        energy = beta_energies
        spectrum = beta_nu
    
    # if there is both beta decay AND electron capture
    elif beta_pathes != [] and ec_pathes != [] :

        # Fixing that beta energies is off by one due to normalization
        ec_energies.ptp(0)
        ec_nu.pop(0)

        if beta_energies[-1] > ec_energies[-1] :
            energy = beta_energies
            max_nu = beta_nu
            min_energies = ec_energies
            min_nu = ec_nu

        else :
            energy = ec_energies
            max_nu = ec_nu
            min_energies = beta_energies
            min_nu = beta_nu

        for e in energy :
            if e in min_energies :
                spectrum.append(max_nu[int(e)-1] + min_nu[int(e)-1])
            else : 
                spectrum.append(max_nu[int(e)-1])

    # Plot Complete Spectrum
    iso_name = start[0]
    plot(energy, spectrum, 'Neutrino', iso_name)
    if beta_pathes != [] :
        plot(beta_energies, beta_beta, 'Beta', iso_name)

    # Save Spectrum Data as a CSV File
    make_csv(energy, spectrum, 'Neutrino', iso_name)
    if beta_pathes != [] :
        make_csv(beta_energies, beta_beta, 'Beta', iso_name)