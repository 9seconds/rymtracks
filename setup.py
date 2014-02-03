#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from sys import version_info as python_version
from setuptools import setup, find_packages


##############################################################################


REQUIREMENTS = [
    "tornado==3.2",
    "beautifulsoup4==4.3.2",
    "lxml==3.3.0",
    "isodate==0.4.9",
    "docopt==0.6.1",
    "nose==1.3.0",
    "six==1.5.2"
]
if python_version >= (3,):
    REQUIREMENTS.append("futures==2.1.6")

with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    long_description=LONG_DESCRIPTION,
    version="0.1.2",
    packages=find_packages(exclude=["tests"]),
    setup_requires=["nose>=1.0"],
    install_requires=REQUIREMENTS,
    author="Sergey Arkhipov",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    zip_safe=False,
    maintainer_email="serge@aerialsounds.org",
    entry_points=dict(console_scripts=["rymtracks = rymtracks:main"]),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "Topic :: Utilities"
    ],
    test_suite="nose.collector",
    url="https://github.com/9seconds/rymtracks/",
)
