#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

REQUIRED = [
    'lxml',
    'selenium',
    'dateparser',
    'pyTelegramBotAPI',
]

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open("spb_dnevnik_bot/__about__.py") as fp:
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
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

)
