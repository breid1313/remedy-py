# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setup(
    name="remedy_py",
    version="1.0.0",
    description="A python package used to interface with the BMC Remedy ITSM REST API",
    license="MIT",
    author="Brian Reid",
    url="https://github.com/breid1313/remedy-py",
    packages=find_packages(),
    install_requires=["requests"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
