from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sins',
    version='0.1.0',
    description='A Python package designed to create neutrino spectra for the radioactive decay of any isotope.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shortlab/2024-bnryan-single-isotope-neutrino-spectrum-generator',
    author='Brianna Noelani Ryan',
    author_email='bnryan@mit.edu',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'matplotlib>=2.0.0',
        'numpy>=1.15.0',
        'scipy>=1.2.0',
        'scikit-learn>=0.20.0',
    ],
    license='BSD-2-Clause',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Physics',
    ]
)