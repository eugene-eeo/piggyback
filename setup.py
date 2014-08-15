#!/usr/bin/env python
import piggyback
from distutils.core import setup
from setuptools import find_packages

setup(
    name='Piggyback',
    version=piggyback.__version__,
    description='Recursive module importer',
    author='Eugene Eeo',
    author_email='packwolf58@gmail.com',
    url='https://github.com/eugene-eeo/piggyback',
    packages=['piggyback'],
)
