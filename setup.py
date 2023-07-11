#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

import setuptools


# Package meta-data.
NAME = 'to_tmx'
DESCRIPTION = 'Txt-to-tmx file converter.'
URL = 'https://github.com/AlexSkrn/to_tmx'
EMAIL = 'alex.g.skrn@gmail.com'
AUTHOR = 'AlexSkrn'
REQUIRES_PYTHON = '>=3.6.0'


def list_reqs(fname='requirements.txt'):
    """Return a list of packages required for this module to be executed."""
    with open(fname) as fd:
        return fd.read().splitlines()


here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'readme.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


setuptools.setup(
    name=NAME,
    version='1.0.2',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=list_reqs(),
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
    keywords='tmx converter',
    entry_points={
        'console_scripts': [
            'sent-tok=to_tmx.sent_tok:main',
            'to-tmx=to_tmx.to_tmx:main',
            'tmx-tradosize=to_tmx.tmx_tradosizer:main',
            'tmx-batch-tradosize=to_tmx.tmx_batch_tradosizer:ProcessTMX'
        ],
    },
)
