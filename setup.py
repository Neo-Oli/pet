#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, print_function
from pet import __version__
import sys


try:
	from setuptools import setup
except ImportError:
	print(
		'You do not have setuptools, and can not install pet. The easiest '
		'way to fix this is to install pip by following the instructions at '
		'http://pip.readthedocs.org/en/latest/installing.html\n'
		'Alternately, you can run sopel without installing it by running '
		'"python sopel.py"',
		file=sys.stderr,
	)
	sys.exit(1)
def read_reqs(path):
	with open(path, 'r') as fil:
			return list(fil.readlines())

requires = read_reqs('requirements.txt')
setup(
    name='pet',
    version=__version__,
    description='Tamagotchi clone for the terminal ',
    author='Oliver Schmidhauser',
    author_email='oliver.schmidhauser@gmail.com',
		url='http://github.com/Neo-Oli/pet',
    long_description=(
        "Virtual pet simulator"
    ),
    packages=[str('pet')],
		data_files=[('translations', ['translations/en.yml','translations/de.yml']),
							 ('config',['config/default.yml'])],
    license='',
    platforms='Linux x86, x86-64',
    install_requires=requires,
    entry_points={'console_scripts': ['pet=pet.run:main']},
)
