#!/usr/bin/env python3

from setuptools import setup
from splashpaper import About

with open("README.md") as file:
    long_description = file.read()

setup(
    name="splashpaper",
    version=About.version,
    author=About.author,
    author_email=About.author_email,
    url=About.url,
    py_modules=["splashpaper"],
    description=About.description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=About.license,
    install_requires=["requests"],
    classifiers=About.classifiers,
    python_requires=">=3.6",
)