from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="transformations2log",
    version="0.0.1",
    description=" A simple package to extract torchvision transformations used during training and testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Danilo Weber Nunes",
    author_email="danilownunes@gmail.com",
    url="https://github.com/danilown/transformations2log",
    license="MIT",
    packages=find_packages(),
)
