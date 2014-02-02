#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from sys import version_info as python_version
from setuptools import setup, find_packages


##############################################################################


REQUIREMENTS = []
with open("requirements.txt", "r") as resource:
    for line in resource.readlines():
        line = line.strip()
        if line and not line.startswith("#"):
            REQUIREMENTS.append(line)


if python_version >= (3,):
    REQUIREMENTS = [
        req for req in REQUIREMENTS if not req.startswith("futures==")
    ]


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    long_description="RYMTracks scraps given URLs and presents tracklists "
                     "into copypasteable form for RateYourMusic.com.\n\n"
                     "For more comprehensive documentation please visit "
                     "https://github.com/9seconds/rymtracks/",
    version="0.1.0",
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
