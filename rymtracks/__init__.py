#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RYMTracks scraps given URLs and presents tracklists into copypasteable form
for RateYourMusic.com.

Usage:
    rymtracks <url>...
    rymtracks -f <filename>
    rymtracks -l
    rymtracks --update-languages
    rymtracks (-h | --help)
    rymtracks --version

Options:
    -h --help           Show this screen.
    --version           Show version.
    --update-languages  Installs languages datafiles for proper RYM
                        capitalization
    -f                  Filename with urls.
    -l                  Show parseable network locations.
"""


from .core import execute
from .formatters import console
from .services import Service

from os import makedirs
from os.path import expanduser, exists, join
from shutil import rmtree
from sys import exit as sysexit

from docopt import docopt
from nltk import download, data as NLTK_DATA
from six import print_, text_type


##############################################################################


__version__ = 0, 1, 2
__all__ = 'main',


##############################################################################


DATA_HOME = join(expanduser("~"), ".rymtracks")
NLTK_DATA_HOME = join(DATA_HOME, "nltk")
NLTK_DATA.path[0:0] = [NLTK_DATA_HOME]


##############################################################################


from nltk import sent_tokenize
try:
    sent_tokenize("")
except LookupError:
    sysexit(
        "No language datafiles found. Please run "
        "'rymtracks --update-languages'."
    )


##############################################################################


def print_service_locations():
    for key in Service.network_locations():
        print_(key)


def update_languages():
    if not exists(DATA_HOME):
        makedirs(DATA_HOME)
    rmtree(NLTK_DATA_HOME, True)
    makedirs(NLTK_DATA_HOME)

    for data in ("stopwords", "punkt", "maxent_treebank_pos_tagger"):
        download(data, download_dir=NLTK_DATA_HOME)


def main():
    """
    Main function. rymtracks script executes this.
    """
    opts = docopt(
        __doc__,
        version="RYMTracks {}".format(
            ".".join(str(num) for num in __version__)
        )
    )

    urls = [text_type(url) for url in opts["<url>"]]
    if opts["<filename>"]:
        with open(opts["<filename>"], "r") as res:
            urls.extend(text_type(url) for url in res.readlines())
    if opts["-l"]:
        return print_service_locations()
    if opts["--update-languages"]:
        return update_languages()
    console(execute(urls))


##############################################################################


if __name__ == "__main__":
    sysexit(main())
