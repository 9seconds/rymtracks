#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from sys import version_info as python_version
from setuptools import setup, find_packages


##############################################################################


REQUIREMENTS = [
    "beautifulsoup4==4.3.2",
    "lxml==3.3.0",
    "isodate==0.4.9",
    "docopt==0.6.1",
    "nose==1.3.0",
    "six==1.5.2",
    "nltk==2.0.4",
    "numpy==1.8.0",
    "requests==2.2.1",
    "colorama==0.2.7",
    "termcolor==1.1.0"
]


##############################################################################


if python_version < (3,):
    REQUIREMENTS.extend(
        [
            "futures==2.1.6",
            "mutagen==1.22"
        ]
    )
else:
    REQUIREMENTS.append("mutagenx==1.22")

with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    long_description=LONG_DESCRIPTION,
    version="0.1.4",
    author="Sergey Arkhipov",
    license="MIT",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    maintainer_email="serge@aerialsounds.org",
    url="https://github.com/9seconds/rymtracks/",
    install_requires=REQUIREMENTS,
    tests_require=["nose==1.3.0"],
    packages=find_packages(exclude=["tests"]),
    entry_points=dict(console_scripts=["rymtracks = rymtracks:main"]),
    test_suite="nose.collector",
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
    zip_safe=False
)
