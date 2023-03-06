# -*- coding: utf-8 -*-
"""Setup for sos-ansible"""
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as file:
    readme = file.read()

with open("LICENSE", encoding="utf-8") as file:
    license = file.read()  # pylint: disable=redefined-builtin

setup(
    name="sos_ansible",
    version="0.1.0",
    description="sos_ansible package",
    long_description=readme,
    author="Lucas Benedito",
    author_email="llucasdias@icloud.com",
    url="https://github.com/lucas-benedito/sos-ansible",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
