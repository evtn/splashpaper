#!/usr/bin/env python3

from setuptools import setup

# this is deprecated. use pyproject.toml
class About:
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]

    title = "splashpaper"
    description = "Wallpaper manager with unsplash.com integration"
    version = "1.3.3"
    author = "evtn"
    author_email = "g@evtn.ru"
    license = "MIT"
    url = "https://github.com/evtn/splashpaper"

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