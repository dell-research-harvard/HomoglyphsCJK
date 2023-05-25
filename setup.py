import os
from setuptools import find_packages, setup

with open("README.md","r") as fh:
    long_des = fh.read()

setup(
    name="HomoglyphsCJK",
    packages=["HomoglyphsCJK"],
    version="0.1.0",
    author="HomoglyphsCJK Team",
    author_email="homoglyphscjk@gmail.com",
    description="An easy Python package for fuzzy matching Chinese(simplified and traditional), Japanese and Korean, using character similarity trained from ViT transformer",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://github.com/dell-research-harvard/HomoglyphsCJK.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[            # I get to this in a second
          'gdown==4.7.1',
          'pandas',
          'tqdm',
          'numpy',
          'multiprocess'
    ]
)
