# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Palinka',
    version='0.1.0',
    description='Turns automation code into a plant simulation',
    long_description=readme,
    author='Gaël Pabois',
    author_email='gael.pabois@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    zip_safe=False
)

