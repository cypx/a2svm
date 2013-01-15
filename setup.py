#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
execfile('a2svm/ressources.py')
 
setup(
    name='a2svm',
    version=__version__,
    packages=find_packages(),
    author=__author__,
    author_email="cyp@bidouille.info",
    description=__description__,
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=['appdirs','argparse'],
    url='https://github.com/cypx/a2svm',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: Debian",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ],
    entry_points = {
        'console_scripts': [
            'a2svm = a2svm.a2svm:launcher',
        ],
    },
    license=__license__,
 
) 
