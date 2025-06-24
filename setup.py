from setuptools import setup

setup(
    name='sins',
    version='0.1.0',    
    description='A python pacakged designed to create neutrino spectra for ' + \
                'the radioactive decay of any isotope.',
    url='https://github.com/shortlab/2024-bnryan-single-isotope-neutrino-spectrum-generator',
    author='Brianna Noelani Ryan',
    author_email='bnryan@mit.edu',
    #license='BSD 2-clause',
    packages=['sins'],
    install_requires=['matplotlib',
                      'numpy', 
                      'scipy',  
                      'scikit-learn',                    
                      ]

    #classifiers=[
    #    'Development Status :: 1 - Planning',
    #    'Intended Audience :: Science/Research',
    #    'License :: OSI Approved :: BSD License',  
    #    'Operating System :: POSIX :: Linux',        
    #    'Programming Language :: Python :: 2',
    #    'Programming Language :: Python :: 2.7',
    #    'Programming Language :: Python :: 3',
    #    'Programming Language :: Python :: 3.4',
    #    'Programming Language :: Python :: 3.5',
    #],
)