# __main__.py
#!/usr/bin/env python
# coding: utf-8

##########################
### Imports & Variables
##########################

import csv
import matplotlib.pyplot as plt

from .beta import beta_decay_spectrum
from .ec import ec_spectrum 

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
               The name of the csv file containing the starting isotope and 
               it's decay paths.

    Returns
    --------
    start_iso: tuple 
               The information about the initial isotope. Follows the format 
               (Decay Type, Isotope, Z, A, Spin, Parity, Q, Branching Ratio)
    beta_pathes: list
                 This list contains the tuples of information for the beta 
                 decay pathes of the starting isotope
    ec_pathes: list
               This list contains the tuples of information for the electron 
               capture decay pathes of the starting isotope
    '''
    # Check for Basic Errors with the File
    if type(file_name) != str :     # Check that file name was given as a string
        raise TypeError('The file name must be inputted as a string.') 
    
    if file_name.endswith('.csv') == False :        # Check that a csv file was provided
        if file_name.endswith('.txt') == True :     # If a txt file was provided, convert it to a csv file
            with open(file_name, 'r') as in_file:
                stripped = (line.strip() for line in in_file)
                lines = (line.split(",") for line in stripped if line)
                csv_file_name = file_name[:-4] + '.csv'
                with open(csv_file_name, 'w') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow(('title', 'intro'))                        
                    writer.writerows(lines)
                file_name = csv_file_name
        else :
            raise Exception('The given file is not a CSV file. Please supply a CSV file.')
    
    # Open and prepare csv file
    with open(file_name) as file :
        reader = csv.reader(file)
        header = next(reader)

        beta_pathes = []
        ec_pathes = []

        # Read each row
        for row in reader :

            # Check to make sure file is written in the proper format
            if len(row) != 8 :      # Check there is 8 elements in each row
                raise Exception('CSV file is not the right dimensions. Please make sure each row has a value for Decay Type, Isotope, Z, A, Spin, Parity, Q, and Branching Ratio.')
        
            if row[0].lower() not in ('start','beta','ec') :     # Check that Decay Types were written properly
                if row[0].lower() == 'electron capture' : 
                    row[0] = 'EC'
                else :
                    raise Exception('Decay type (' + str(row[0]) + ') not written properly. Please either use Start, Beta, or EC.')
            
            # Check to make sure each value is the correct type
            try :       # Are all Z values integers
                value = int(row[2])
            except ValueError :
                print('One of your Z values (' + row[2] + ') is not an integer.')

            try :       # Are all A values integers
                value = int(row[3])
            except ValueError :
                print('One of your A values (' + row[3] + ') is not an integer.')
            
            try :       # Are all Spin values floats
                value = float(row[4])
            except ValueError :
                print('One of your spin values (' + row[4] + ') is not a number.')

            try :       # Are all Parity values integers
                value = float(row[5])
            except ValueError :
                print('One of your parity values (' + row[5] + ') is not an integer.')

            try :       # Are all Q values floats
                value = float(row[6])
            except ValueError :
                print('One of your Q values (' + row[6] + ') is not a number.')

            try :       # Are all Branching Ratio values floats
                value = float(row[7])
            except ValueError :
                print('One of your branching ratio values (' + row[7] + ') is not a number.')

            # Define Starting Isotope and Different Pathes
            if row[0].lower() == 'start' :
                start_iso = (row[1], int(row[2]), int(row[3]), float(row[4]), \
                                 int(row[5]), float(row[6]), float(row[7]))

            if row[0].lower() == 'beta' :
                beta_pathes.append((row[1], int(row[2]), int(row[3]), float(row[4]), \
                                    int(row[5]), float(row[6]), float(row[7])))

            if row[0].lower() == 'ec' :
                ec_pathes.append((float(row[6]), float(row[7])))

    return start_iso, beta_pathes, ec_pathes

###################
### Usable Functions
###################

def generate(file_name, gen_files) :
    ''' 
    Goal: Generate Neutrino Spectrum

    Parameters
    -----------
    file_name: str
               A string containing the name of the csv file with the decay paths.

    Potential Returns
    -----------------
    energy: list
            A list of the energies (in keV) that neutrinos from this isotope may 
            have. This list is always returned.
    spectrum: list
              A list of the neutrino spectrum values (per keV per decay). This 
              list is always returned.
    beta_energies: list 
                   A list of the energies (in keV) that betas from this isotope 
                   may have. This list is only returned if the isotope decays 
                   via beta decay and beta_energies does not equal energy.
    beta_beta: list
               A list of the beta spectrum values (per keV per decay). This list 
               is only returned if the isotope decays via beta decay.
    '''

    # Read Input File
    start, beta_pathes, ec_pathes = read_file(file_name)
    print(start)
    
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
    
    if gen_files == True :
        # Plot Complete Spectrum
        iso_name = start[0]
        plot(energy, spectrum, 'Neutrino', iso_name)
        print('File Created: ' + iso_name + '_' + 'Neutrino_Spectrum.png')
        if beta_pathes != [] :
            plot(beta_energies, beta_beta, 'Beta', iso_name)
            print('File Created: ' + iso_name + '_' + 'Beta_Spectrum.png')

        # Save Spectrum Data as a CSV File
        make_csv(energy, spectrum, 'Neutrino', iso_name)
        print('File Created: ' + iso_name + '_' + 'Neutrino_Spectrum.csv')
        if beta_pathes != [] :
            make_csv(beta_energies, beta_beta, 'Beta', iso_name)
            print('File Created: ' + iso_name + '_' + 'Beta_Spectrum.csv')

    # Return the proper values
    if beta_pathes == [] :
        return energy, spectrum
    elif ec_pathes == [] :
        return energy, spectrum, beta_beta
    elif beta_pathes != [] and ec_pathes != [] :
        return energy, spectrum, beta_energies, beta_beta 

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
    print('File Created: ' + iso_name + '_' + particle + '_Spectrum.png')
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

    print('File Created: ' + iso_name + '_' + particle + '_Spectrum.csv')
