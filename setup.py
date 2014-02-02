#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from rymtracks import __version__

from sys import version_info as python_version
from setuptools import setup, find_packages


##############################################################################


REQUIREMENTS = []
with open("requirements.txt", "r") as resource:
    for line in resource.readlines():
        line = line.strip()
        if line and not line.startswith("#"):
            REQUIREMENTS.append(line)


EXTRAS = {}
if python_version >= (3,):
    EXTRAS["2to3"] = True


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    version=".".join(str(chunk) for chunk in __version__),
    packages=find_packages(),
    setup_requires=["nose>=1.0"],
    install_requires=REQUIREMENTS,
    author="Sergey Arkhipov",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    zip_safe=True,
    maintainer_email="serge@aerialsounds.org",
    entry_points=dict(console_scripts=["rymtracks = rymtracks:main"]),
    license="MIT",
    test_suite='nose.collector',
    url="https://github.com/9seconds/rymtracks/",
    **EXTRAS
)
