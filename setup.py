#!/usr/bin/env python

"""
HK Dataminer
A python library for constructing statistical models for bimolecular dynamics data.
"""
import sys
from setuptools import setup, find_packages

short_description = __doc__.split("\n")


setup(name='hkdataminer',
      version='1.0',
      description='Python Distribution Utilities',
      author='Song Liu, Hanlin Gu, Xuhui Huang',
      author_email='n/a',
      url='https://github.com/liusong299/HK_DataMiner',
      packages=find_packages(),
     )
