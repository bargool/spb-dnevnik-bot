#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

with open(here / 'requirements.txt', encoding='utf-8') as reqs:
    required = reqs.read().splitlines()

with io.open(here / 'README.rst', encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(here / 'spb_dnevnik_bot' / '__about__.py') as fp:
    exec(fp.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=long_description,
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__uri__'],
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['dnevnik-bot=spb_dnevnik_bot.main:main'],
    },
    install_requires=required,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

)
