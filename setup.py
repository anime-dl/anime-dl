#!/usr/bin/env python3

from setuptools import setup, find_packages
import re
import io


with io.open('anime_dl/__version__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open("requirements.txt", "r", encoding="utf8") as f:
    requirements = [x.strip() for x in f.readlines()]

setup(
    name='anime-dl',
    version=version,
    author='ArjixWasTaken',
    author_email='arjixg53@gmail.com',
    description='Download your favourite anime',
    packages=find_packages(),
    url='https://github.com/anime-dl/anime-downloader',
    keywords=['anime', 'downloader', 'download'],
    install_requires=requirements
)
