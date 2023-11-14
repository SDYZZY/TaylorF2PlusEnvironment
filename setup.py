#!/usr/bin/env python
"""
setup.py file pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

VERSION = '0.0.dev1'

setup (
    name = 'TaylorF2PlusEnvironment',
    version = VERSION,
    description = 'A simplified waveform plugin which based on the PN wavefrom from "Physics Astrophysics And Cosmolog with Gravitational Waves". And I added some environmental effects in it.',
    long_description = open('README.md').read(),
    author = 'SDYZZY',
    author_email = 'sdyzzy@mail.ustc.edu.cn',
    url = 'http://www.pycbc.org/',
    download_url = 'https://github.com/gwastro/revchirp/tarball/v%s' % VERSION,
    keywords = ['pycbc', 'test', 'gravitational waves'],
    install_requires = ['pycbc'],
    py_modules = ['TaylorF2PlusEnvironment'],
    entry_points = {"pycbc.waveform.fd":"TaylorF2PlusEnvironment=TaylorF2PlusEnvironment:TaylorF2PlusEnvironmentFrequencyDomainPlusCross",
                    "pycbc.waveform.length":"TaylorF2PlusEnvironment=TaylorF2PlusEnvironment:Taylor_duration"},

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)

# entry_points: "capability":"approximant_name = module_path:function_name"
