#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for RYMTracks.
"""


from distutils.command.install_data import install_data
from sys import version_info as python_version
from setuptools import setup, find_packages
from setuptools.command.install import install


##############################################################################


class UpdateNLTKData(install_data):
    """
    Updater of NLTK data
    """

    def run(self):
        from os import makedirs
        from os.path import expanduser, exists, join
        from shutil import rmtree
        from nltk import download

        home_directory = join(expanduser("~"), ".rymtracks")
        nltk_data_directory = join(home_directory, "nltk")
        if not exists(home_directory):
            makedirs(home_directory)
        rmtree(nltk_data_directory, True)
        makedirs(nltk_data_directory)

        for data in ("stopwords", "punkt", "maxent_treebank_pos_tagger"):
            download(data, download_dir=nltk_data_directory)


class Install(install):
    """
    Custom procedure which updates NLTK data on install
    """

    def do_egg_install(self):
        install.do_egg_install(self)
        self.run_command("update_nltk_data")


##############################################################################


REQUIREMENTS = [
    "tornado==3.2",
    "beautifulsoup4==4.3.2",
    "lxml==3.3.0",
    "isodate==0.4.9",
    "docopt==0.6.1",
    "nose==1.3.0",
    "six==1.5.2",
    "nltk==2.0.4",
    "numpy==1.8.0"
]

EXTRAS = {}


##############################################################################


if python_version < (3,):
    REQUIREMENTS.append("futures==2.1.6")
    EXTRAS["cmdclass"] = {
        "install": Install,
        "update_nltk_data": UpdateNLTKData
    }
    EXTRAS["setup_requires"] = ["nltk==2.0.4"]

with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


##############################################################################


setup(
    name="RYMTracks",
    description="RYMTracks scraps given URLs and presents tracklists into "
                "copypasteable form for RateYourMusic.com",
    long_description=LONG_DESCRIPTION,
    version="0.1.3",
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
    zip_safe=False,
    **EXTRAS
)
