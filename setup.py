#! /usr/bin/env python
from setuptools import setup, find_packages
from io import open

setup(
    name='media-auditor',
    packages=find_packages(exclude=['testing']),
    version='0.1',
    description='A commandline tool for automatically cataloging'
                'media quality',
    author='Dillon Dixon',
    author_email='dillondixon@gmail.com',
    url='https://github.com/ownaginatious/media-auditor',
    download_url='https://github.com/ownaginatious'
                 '/media-auditor/tarball/0.1',
    license='MIT',
    keywords=['python'],
    classifiers=['Environment :: Console'],
    install_requires=[line.strip()
                      for line in open("requirements.txt", "r",
                                       encoding="utf-8").readlines()],
    entry_points={
        "console_scripts": [
            "mediaaudit = media_auditor.main:main",
        ],
    }
)
