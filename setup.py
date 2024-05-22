from setuptools import find_packages
from setuptools import setup


with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


setup(
    name="OpenFASoC",
    version="0.0.1",
    url="https://github.com/idea-fasoc/OpenFASOC",
    license="MIT",
    author=" msaligane",
    author_email="mehdi@umich.edu",
    description="Fully Open-Source Autonomous SoC Synthesis using Customizable Cell-Based Synthesizable Analog Circuits",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    install_requires=get_install_requires(),
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
)
