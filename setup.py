from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.readlines()

setup(
    name="transformations2log",
    version="0.0.1",
    description="Simple class to make Pytorch dataset object creation easier and more flexible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Danilo Weber Nunes",
    author_email="danilownunes@gmail.com",
    url="https://github.com/danilown/transformations2log",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(),
)
