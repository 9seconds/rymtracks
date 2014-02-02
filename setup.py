#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from rymtracks import __version__

from setuptools import setup, find_packages


##############################################################################


REQUIREMENTS = []
with open("requirements.txt", "r") as resource:
    for line in resource.readlines():
        line = line.strip()
        if line and not line.startswith("#"):
            REQUIREMENTS.append(line)


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    version=".".join(str(chunk) for chunk in __version__),
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    author="Sergey Arkhipov",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    zip_safe=True,
    maintainer_email="serge@aerialsounds.org",
    entry_points=dict(console_scripts=["rymtracks = rymtracks:main"]),
    license="MIT",
    url="https://github.com/9seconds/rymtracks/"
)
