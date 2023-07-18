#!/usr/bin/env python3
from setuptools import setup, find_packages

from utilities import __version__

requirements = open("requirements.txt").read().strip().split("\n")

setup(
    name="utilities",
    packages=find_packages(),
    version=__version__,
    description="efabless caravel user project.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Marwan Abbas",
    author_email="marwan.abbas@efabless.com",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "utilities": ["helper_lib/*", "helper_lib/**/*", "helper_lib/**/**/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Users",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    entry_points={"console_scripts": ["utilities = utilities.__main__:cli"]},
    python_requires=">3.6",
)
