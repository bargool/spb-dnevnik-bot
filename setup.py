#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'spb-dnevnik-bot'
DESCRIPTION = 'Telegram bot for school journal at petersburgedu.ru'
URL = 'https://github.com/bargool/spb-dnevnik-bot'
EMAIL = 'bargool@gmail.com'
AUTHOR = 'Aleksey Nakoryakov'

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
with open("spb-dnevnik-bot/__about__.py") as fp:
    exec(fp.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
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
