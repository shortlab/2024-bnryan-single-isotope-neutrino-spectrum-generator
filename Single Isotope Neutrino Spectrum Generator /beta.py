#!/usr/bin/env python
# coding: utf-8

##########################
### Imports & Constants
##########################

### Imports
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma
from scipy.constants import physical_constants
from sklearn import preprocessing

### Define Constants
keV = 1.
electron_mass = 510.9989461 * keV
α = physical_constants['fine-structure constant'][0]

#############################################
### Defining Classes
### Written by: Professor Joseph Formaggio
#############################################

class Isotope:
    def __init__(self, Name, AtomicNumber, AtomicMass, JSpin, Parity):
        self.Name = Name
        self.AtomicNumber = AtomicNumber
        self.AtomicMass = AtomicMass
        self.JSpin = JSpin
        self.Parity = Parity

class DecayProcess:
    def __init__(self, parentAtom, progenyAtom, decayType, deltaJ, deltaP, QValue):
        self.parentAtom = parentAtom
        self.progenyAtom = progenyAtom
        self.decayType = decayType
        self.deltaJ = deltaJ
        self.deltaP = deltaP
        self.QValue = QValue

##############################################
### Generating the Spectra
### Written by: Professor Joseph Formaggio
##############################################

def SetDecayProcess(Parent, Progeny, QValue):
    dJ = int(abs(Parent.JSpin - Progeny.JSpin))
    dP = int(np.sign(Parent.Parity * Progeny.Parity))   
    return DecayProcess(Parent, Progeny, "β-", dJ, dP, QValue)

def ν(x):
    # Normalize energy by electron mass
    return x / electron_mass + 1

def df2(n):
    # Double factorial implementation
    return np.prod(np.arange(n, 1, step=-2))
            # Okay I have never used a double factorial so???

def R(Z, A=0):
    # Nuclear radius calculation
    # If A is not specified, reconstruct from Z
    # Inputs:  Z (nuclear charge), A (atomic numer)
    # Output:  Nuclear radius
    if A < 1:
        A = 1.82 + 1.90 * Z + 0.01271 * Z**2 - 0.00006 * Z**3
    radius = (0.002908 * A**(1/3) - 0.002437 * A**(-1/3))
    return radius

def p(W, 𝜈=1):
    # Particle normalized momentum (defaults to electron if 𝜈 is unspecified)
    # Inputs: W (normalized energy)
    # Outputs: p (normalized momentum)
    return np.sqrt(W**2 - 𝜈**2) if W >= 𝜈 else 0
            # This line looks like it could vary from mine

def μ(k, Z, W, A=0):
    # Coulomb amplitudes for the beta decay process
    # For k = 1, this is the Fermi function
    # Inputs: 
    #         k (iteration term in sum)
    #         W (normalized electron energy)
    #         Z (progeny charge)
    #         A (atomic mass)
    # Outputs: μ (Coulomb amplitude term for k)
    l = np.sign(k)
    γ = np.sqrt(k**2 - α**2 * Z**2)
    y = α * Z * W / p(W)
    
    𝛋 = γ + 1j * y   
    β = 2 * γ + 1
    omega = 2 * p(W) * R(Z, A)
    
    # ϕ = -(k - 1j * y) * (hyp1f1(𝛋 + 1, β, 1j * omega) - l * (γ - 1j * y * hyp1f1(𝛋, β, 1j * omega)))
    ϕ = np.sqrt(2 * (γ + 1))
    Ω = np.sqrt(np.abs(1 - l * W)) * (omega)**γ * np.exp(np.pi * y / 2) * np.abs(gamma(𝛋)) / gamma(β)
    result = Ω * ϕ / (2 * R(Z, A) * np.sqrt(W))
    return result

def wave_func(k, Z, W, A=0, lambda_appproximation=True):
    # Sum of Coulomb ampliutudes to form electron wave function
    # Inputs: 
    #         k (iteration term in sum)
    #         W (normalized electron energy)
    #         Z (progeny charge)
    #         l (angular momentum term)
    #         A (atomic mass)
    # Outputs: wave_func (electron wave function)
    #          Defaults to 1 in the lambda=1 appproximation
    k_eff = 1 if lambda_appproximation else k
    term1 = abs(μ(k_eff, Z, W, A))**2 + abs(μ(-k_eff, Z, W, A))**2
    term2 = abs(μ(1, Z, W, A))**2 + abs(μ(-1, Z, W, A))**2
    result = term1 / term2
    return result

def Fermi_func(Z, W, A=0):
    # Fermi function based on Coulomb amplitudes
    return (abs(μ(1, Z, W, A))**2 + abs(μ(-1, Z, W, A))**2) / (2 * p(W)**2)

def shape_factor(n, Z, W, p_e, p_ν, A=0):
    # Function that computes the partial matrix elements and the Fermi function for the beta decay process
    sum = 0.0
    for k in range(1, n+2):
        sum += wave_func(k, Z, W, A) * p_e**(2 * (k - 1)) * p_ν**(2 * (n - k + 1)) / df2(2 * k - 1) / df2(2 * (n - k + 1) + 1)
    return df2(2 * n + 1) * sum

def β_spectrum(W_e, W_ν, p_e, p_ν, n, Z, A=0):
    # Calculate neutrino or electron beta decay spectrum
    C_W = shape_factor(n, Z, W_e, p_e, p_ν, A)
    F_Z = Fermi_func(Z, W_e)
    phase_space = (p_e * W_e) * (W_ν * p_ν)
    return F_Z * C_W * phase_space 

def beta_spectrum(process, K_e):
    # Beta electron spectrum
    Q = process.QValue
    Z = process.progenyAtom.AtomicNumber
    A = process.parentAtom.AtomicMass
    n = max(process.deltaJ - 1, 0)
    
    W_e = ν(K_e)          # Total electron energy
    W_ν = ν(Q) - W_e      # Total neutrino energy
    p_e = p(W_e, 1)       # Electron momentum
    p_ν = p(W_ν, 0)       # Neutrino momentum
    
    return β_spectrum(W_e, W_ν, p_e, p_ν, n, Z, A)

def neutrino_spectrum(process, K_ν):
    # Beta neutrino spectrum
    Q = process.QValue
    Z = process.progenyAtom.AtomicNumber
    A = process.parentAtom.AtomicMass
    n = max(process.deltaJ - 1, 0)

    W_e = ν(Q - K_ν)       # Total electron energy
    W_ν = ν(K_ν) - 1       # Total neutrino energy
    p_ν = p(W_ν, 0)        # Neutrino momentum
    p_e = p(W_e, 1)        # Electron momentum
    
    return β_spectrum(W_e, W_ν, p_e, p_ν, n, Z, A)

def Γ_beta(process):
    # Integrated beta electron spectrum
    Q = process.QValue
    result, _ = quad(lambda K: beta_spectrum(process, K), 0, Q)
    return max(result, 0)

def Γ_ν(process):
    # Integrated beta electron spectrum
    Q = process

### Normalizing Spectra
def normalize(data, energies, path):
    data = data[1:-1]
    norm_num = preprocessing.normalize([data])
    
    sum_track = 0
    for i in norm_num[0] :
        sum_track = sum_track + (i*path[5]/len(energies-2))
    
    num_final = []
    for i in norm_num[0] :
        num_final.append(i/sum_track*path[6])
        
    return num_final

### Run all Spectra Functions
def run_path(start, path) :
    ''' 
    Goal: Run the complete fermi approximation for a single path.

    Parameters
    -----------
    start: tuple
           The information about the initial isotope. Follows the format (Isotope, Z, A, Spin, Parity, Q, Branching Ratio)
    path: tuple
          The information about the chosen decay path. Follows the format (Isotope, Z, A, Spin, Parity, Q, Branching Ratio)
               
    Returns
    --------
    beta_final: list
                The total fermi approximated beta spectrum for this path.
    nu_final: list
                The total fermi approximated neutrino spectrum for this path.
    energies: list
              A list of the energies (in keV) that particles from this decay path may have.
    '''
    
    energies = np.linspace(0, int(path[5]), int(path[5]) + 1)
    start_iso = Isotope(start[0], start[1], start[2], start[3], start[4])
    end_iso = Isotope(path[0], path[1], path[2], path[3], path[4])
    beta = SetDecayProcess(start_iso, end_iso, int(path[5]))

    s = [beta_spectrum(beta, z) for z in energies]
    q = [neutrino_spectrum(beta, z) for z in energies]
    
    beta_final = normalize(s, energies, path)
    nu_final = normalize(q, energies, path)
    energies = energies[1:-1]
        
    return beta_final, nu_final, energies

#################################
### Obtaining Complete Spectra
#################################

def sum_pathes(beta, nu, energies) :
    ''' 
    Goal: Add together all of the sum 

    Parameters
    -----------
    beta: list
           The sets of beta spectra for the corresponding decay pathes.
    nu: list
        The sets of neutrino spectra for the corresponding decay pathes.
    energies: list
              The sets of energies for the corresponding decay pathes.

    Returns
    --------
    total_beta: list
                The total fermi approximated beta spectrum
    total_nu: list
                The total fermi approximated neutrino spectrum
    '''

    total_beta = [0] * len(energies)
    total_nu = [0] * len(energies)
    
    for set in beta :
        for i in range(len(set)) :
            total_beta[i] += set[i]
    
    for set in nu :
        for i in range(len(set)) :
            total_nu[i] += set[i]

    return total_beta, total_nu

#########################
### Combine Everything
#########################

def beta_decay_spectrum(start, beta_pathes) :
    ''' 
    Goal: Generate the neutrino spectrum from beta.

    Parameters
    -----------
    beta_paths: list
                All of the decay paths that are via beta.

    Returns
    --------
    energies: list
              A list of the energies (in keV) that neutrinos from this isotope may have. 
    total_nu: list
              A list of the neutrino spectrum values (per keV per decay). 
    total_beta: list
                A list of the beta spectrum values (per keV per decay). 
    '''

    # Generate Individual Path Spectra
    beta_spectra = []
    nu_spectra = []
    energies = []

    for path in beta_pathes :
        beta, nu, path_energy = run_path(start, path)
        beta_spectra.append(beta)
        nu_spectra.append(nu)
        
        if len(path_energy) > len(energies) :
            energies = path_energy
    
    # Generate Complete Spectra
    total_beta, total_nu = sum_pathes(beta_spectra, nu_spectra, energies)

    return energies, total_beta, total_nu
