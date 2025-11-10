# SINS (Single Isotope Neutrino Spectrum generator) 
This package is designed to create neutrino spectra for the radioactive decay of any isotope. To do this it takes a CSV file of the different decay paths of said isotope, and for those that are beta decay or electron capture, it generates the resulting spectrum for neutrinos per keV per decay.

Authors: B. N. Ryan* & J. A. Formaggio

*bnryan@mit.edu
  
## Table of Contents
1. Installation Instructions
2. Use Instructions

   a. CSV File Construction

   b. Test Cases

3. Methodology
4. References

## 1. Installation Instructions
You can use the package manager [pip](https://pip.pypa.io/en/stable/) to install SINS. Once the repository is downloaded simply run,
```bash
pip install .
```
The other Python packages required to run this package successfully are [sys](https://docs.python.org/3/library/sys.html), [csv](https://docs.python.org/3/library/csv.html), [matplotlib](https://matplotlib.org/), [numpy](https://numpy.org/), [scipy](https://scipy.org/), [sklearn](https://scikit-learn.org/stable/), and [ast](https://docs.python.org/3/library/ast.html). If you do not have them, they should install automatically upon installing sins.

## 2. Use Instructions

### a. CSV File Construction
Writing the proper csv file is essential to the function of this package.  The file should contain 8 columns: Decay Type, Isotope, Z, A, Spin, Parity, Q, and Branching Ratio.  For this information I would recommend using the [KAERI Table of Nuclides](https://atom.kaeri.re.kr/nuchart/) [1] and the [IAEA Table of Nuclides](https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html)[2]. Here is an example csv file for Ir-192, which has both beta and electron capture paths:

```bash
Decay,Isotope,Z,A,Spin,Parity,Q,Branching Ratio
Start,Ir-192,77,192,4.0,1,0,0
Beta,Pt-192,78,192,3.0,1,48.1,0.000059
Beta,Pt-192,78,192,5.0,-1,70.5,0.000039
Beta,Pt-192,78,192,3.0,-1,76.5,0.001026
Beta,Pt-192,78,192,4.0,1,240.0,0.0560
Beta,Pt-192,78,192,3.0,1,535.0,0.4142
Beta,Pt-192,78,192,4.0,1,672.0,0.4798
EC,Os-192,76,192,0.0,1,136.7,0.00094
EC,Os-192,76,192,0.0,1,355.9,0.0393
EC,Os-192,76,192,0.0,1,466.0,0.00670
```
Some important notes when writing these csv files:
- Use Beta and EC as the decay path type labels.
- Make sure your Z, A, and parity can be turned into integers.
- Make sure your spin, Q, and branching ratio can be turned into floats.

### b. Test Cases
In the tests folder there are four different example cases: Cs-137, Cd-109, Co-57, and Ir-192. Each of these includes a properly formatted CSV file describing its decay paths.

To verify that sins is installed and running correctly, a standalone Python test script is provided: sins/test.py.
This script automatically exercises all major components of the package, including:

- read_file() — loads and parses the isotope decay CSV file.

- beta_decay_spectrum() — generates the beta and antineutrino spectra for beta-decay paths.

- ec_spectrum() — generates the neutrino spectrum for electron-capture paths.

- generate() — runs the full workflow and returns computed spectra without saving any files.

To use the test file, simply run:
```bash
python -m sins.test
```

The test script defaults to using the Ir-192 example, but this can be manually changed. If everything is working properly, you should see output similar to the following: 
```bash
Testing with file: ./test_cases/Ir-192/ir-192.csv
read_file: PASS
  start_iso: ('Ir-192', 77, 192, 4.0, 1, 0.0, 0.0)
  beta_pathes count: 6
  ec_pathes count: 3
File Created: Ir-192_Neutrino_Spectrum.png
File Created: Ir-192_Neutrino_Spectrum.png
File Created: Ir-192_Beta_Spectrum.png
File Created: Ir-192_Beta_Spectrum.png
File Created: Ir-192_Neutrino_Spectrum.csv
File Created: Ir-192_Neutrino_Spectrum.csv
File Created: Ir-192_Beta_Spectrum.csv
File Created: Ir-192_Beta_Spectrum.csv
generate function: PASS - returned 4 outputs
```
This confirms that all key functions ran successfully and produced valid spectra. Do not be concerned if you got some divide by zero errors - those are expected. Those errors will look like:
```bash
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/sins/beta.py:89: RuntimeWarning: divide by zero encountered in scalar divide
  y = α * Z * W / p(W)
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/sins/beta.py:97: RuntimeWarning: invalid value encountered in scalar multiply
  Ω = np.sqrt(np.abs(1 - l * W)) * (omega)**γ * np.exp(np.pi * y / 2) * np.abs(gamma(𝛋)) / gamma(β)
```

## 3. Methodology [4][5]
For electron capture, calculating the neutrino energy is simple, as it is equal to the Q value.  For beta decay, it is a bit more complicated.  The methodology, as well as the accuracy of the method used, are elaborated upon here.

To create the antineutrino spectrum I used [Fermi's Theory of Beta Decay](https://pubs.aip.org/aapt/ajp/article/36/12/1150/1047952/Fermi-s-Theory-of-Beta-Decay) [3] and followed the approximations given in [4].  While corrective terms have since been added to Fermi's original theory, they have yet to be added to this package. 

The allowed beta spectrum is given by,

```math
    N_\beta(W_e)=Kp_eW_ep_\nu W_\nu F(Z,W_e)C(W_e),
```
where K is the normalization constant, $p_eW_ep_vW_v$ is the phase space factor, $F(Z,W_e)$ is the Fermi function, and $C(W_e)$ is the theoretical shape factor. All of these factors end up being unitless, and $N_\beta(W_e)$ is defined as the probability of a beta being created at normalized energy $W_e$. As stated in [4], the Fermi function is given by,

```math
    F(Z,W)=2(\gamma+1)(2pR)^{2(\gamma-1)}e^{\pi\alpha ZW/p}\frac{|\Gamma(\gamma+i\alpha ZW/p)|^2}{\Gamma(2\gamma+1)^2},
```

where $\gamma=\sqrt{1-(\alpha Z)^2}$.  For all other variable definitions, see Table 2.2 from [5] (shown below). The momentum and normalized energy definitions are in the $\beta$'s reference frame. Their derivation can be found in Appendix B of [5].

| Symbol | Meaning | Definition |
|--------|---------|------------|
| $E_e$ | Electron Kinetic Energy | Varies | 
| $p_e$ | Normalized Electron Momentum | $\sqrt{\frac{E^2}{m_e^2c^4}+\frac{2E}{m_ec^2}}$ | 
| $p_\nu$ | Normalized Neutrino Momentum | $Q/m_ec^2-E/m_ec^2 $ | 
| $W_e$ | Normalized Electron Energy | $E/m_ec^2+1$ | 
| $W_\nu$ | Normalized Neutrino Energy | $Q/m_ec^2-E/m_ec^2 $ | 
| $W_0$ | Normalized Endpoint Energy | $Q/m_ec^2+1$ | 
| $Q$ | Maximum Energy | Isotope Dependent | 
| $\alpha$ | Fine Structure Constant | 1/137.035999206 | 
| $m_e$ | Electron Mass as Energy | 510.9989461 keV | 
| $R$ | Nuclear Radius | $0.42587\alpha A^{1/3}$ [6] | 
| $Z$ | Proton Number | Isotope Dependent | 
| $A$ | Nucleon Number | Isotope Dependent | 

While $C(W)=1$ for allowed decay paths, it requires more calculation for forbidden decay paths. Allowed decay paths are where the angular momentum of the beta and the antineutrino are zero ($\Delta l=0$).  For forbidden decay paths, the change in angular momentum of these particles is greater than 0.  For the conservation of angular momentum to still hold, this requires both a spin and parity change.  This was originally thought to be forbidden in the laws of physics, but it is now known to be possible, just heavily suppressed due to the parity and spin changes required. There are two types of forbidden decay: unique and non-unique. To determine what type (unique or non-unique) and degree of forbiddenness ($l$) each path is we need to consider change in angular momentum ($I$) and parity ($\Pi$).  From parity, we can determine whether or not $l$ is even or odd using the following equation,

```math
    \Pi_P=\Pi_D*(-1)^l
```

From this equation, it is evident that if there is a change in parity the forbiddenness is odd whereas if there is no change in parity the forbiddenness is even.  From there we know $\Delta I=l+1$ if the decay is unique forbidden and $Delta I=l,l-1$ if the decay is non-unique forbidden.

To find the antineutrino spectrum from the beta spectrum, we have to perform a change of variables to get to the neutrino's reference frame.  This affects the momentum and energies of both the electron and the neutrino.  The definition of these variables in the neutrino's reference frame are given in Table 2.3 from [5] (shown below). Their derivation can be found in Appendix B of [5].

| Symbol | Meaning | Definition |
|--------|---------|------------|
| $E_\nu$ | Neutrino Kinetic Energy | Varies | 
| $p_e$ | Normalized Electron Momentum | $\sqrt{(Q/m_ec^2-E_\nu/m_ec^2+1)^2-1}$ | 
| $p_\nu$ | Normalized Neutrino Momentum | $E_\nu/m_ec^2 $ | 
| $W_e$ | Normalized Electron Energy | $Q/m_ec^2-E_\nu/m_ec^2+1$ | 
| $W_\nu$ | Normalized Neutrino Energy | $E_\nu/m_ec^2$ | 

A statement on the accuracy of this method can be found in Chapter 2.1.1 of [5].

## 4. References
1. Y.-S. Cho, Korea atomic energy research institute table of nuclides, Accessed Jan-May 2024, 2000. url: https://atom.kaeri.re.kr/nuchart/.
2. International Atomic Energy Agency Nuclear Data Section, Iaea table of nuclides, Ac- cessed Jan-May 2024, 2009- 2024. url: https://www-nds.iaea.org/relnsd/vcharthtml/ VChartHTML.html.
3. F. L. Wilson, “Fermi’s Theory of Beta Decay,” Am. J. Phys., vol. 36, no. 12, pp. 1150– 1160, 1968. doi: 10.1119/1.1974382.
4. P. Huber, “Determination of antineutrino spectra from nuclear reactors,” Phys. Rev. C, vol. 84, p. 024 617, 2 Aug. 2011. doi: 10.1103/PhysRevC.84.024617.
5. B. Ryan, Cevns in natural zinc superconductors and its applications for nuclear non-proliferation, chapter 2.1 (2024), https://dspace.mit.edu/handle/1721.1/155639.
6. H. Behrens and J. Jänecke, “Numerical tables for beta-decay and electron capture: Z = 1 - 14,” Group I Elementary Particles, Nuclei and Atoms, vol. 4, H. Schopper, Ed., Springer-Verlag Berlin Heidelberg. doi: 10.1007/10201072_11.
