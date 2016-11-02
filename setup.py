# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.
import re

from codecs import open
from setuptools import setup


with open('pycoreutils/__init__.py', 'r', 'utf-8') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE,
    ).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

with open('README.txt', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='pycoreutils',
    version=version,
    description='Coreutils in Pure Python',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
    ],
    license='MIT',
    url='http://pypi.python.org/pypi/pycoreutils',
    author='Hans van Leeuwen',
    author_email='hansvl@gmail.com',
    scripts=['scripts/pycoreutils'],
    packages=[
        'pycoreutils',
        'pycoreutils.command',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
