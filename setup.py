#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup process."""

from io import open
from os import path

from setuptools import find_packages, setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Basic project information
    name='key_set',
    version='1.0.0',
    # Authorship and online reference
    author='Eduardo Turiño',
    author_email='eturino@eturino.com',
    url='https://github.com/eturino/key_set.py',
    # Detailed description
    description='KeySet with 4 classes to represent concepts of All, None, Some, and AllExceptSome',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='set key_set',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    # Package configuration
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires='>= 3.6',
    install_requires=[],
    # Licensing and copyright
    license='Apache 2.0'
)
