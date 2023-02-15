# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='TemplatePython',
    version='0.1.0',
    description='TemplatePython package',
    long_description=readme,
    author='Lucas Benedito',
    author_email='llucasdias@icloud.com',
    url='https://github.com/lucas-benedito/python_template',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)