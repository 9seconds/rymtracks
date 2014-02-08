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


from os import makedirs
from os.path import exists, expanduser, join as path_join
from shutil import rmtree
from sys import exit as sysexit

from docopt import docopt
from six import print_, text_type, PY2


###############################################################################


__version__ = 0, 1, 3
__all__ = 'main',


###############################################################################


HOME_PATH = path_join(expanduser("~"), ".rymtracks")
NLTK_PATH = path_join(HOME_PATH, "nltk")


###############################################################################


from .core import execute
from .formatters import console
from .services import Service


###############################################################################


def print_service_locations():
    """
    Just prints recognizible network locations.
    """
    for key in Service.network_locations():
        print_(key)


def update_languages():
    """
    Updates NLTK data in your local home. Does nothing on Python 3 because
    NLTK does not support it yet.
    """
    if not PY2:
        return

    from nltk import download

    if not exists(HOME_PATH):
        makedirs(HOME_PATH)
    rmtree(NLTK_PATH, True)
    makedirs(NLTK_PATH)

    for data in ("stopwords", "punkt", "maxent_treebank_pos_tagger"):
        download(data, download_dir=NLTK_PATH)


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
