#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RYMTracks scraps given URLs and presents tracklists into copypasteable form
for RateYourMusic.com.

Usage:
    rymtracks [options] <location>...
    rymtracks --update-languages
    rymtracks -l
    rymtracks (-h | --help)
    rymtracks --version

Options:
    -h --help           Show this screen.
    --version           Show version.
    --update-languages  Installs languages datafiles for proper RYM
                        capitalization
    -f                  Filename with urls.
    -l                  Show parseable network locations.

If you have any question please contact Sergey Arkhipov
(serge@aerialsounds.org) or use GitHub issue tracker:
https://github.com/9seconds/rymtracks/issues
"""


from __future__ import absolute_import, unicode_literals, print_function

import distutils.util
import locale
import os
import os.path
import shutil
import sys

import docopt
import nltk
import six

from .capitalization import capitalize, init as capitalize_init
from .core import execute
from .formatters import console
from .services import Service


###############################################################################


__version__ = 0, 2
__all__ = 'main',


###############################################################################


HOME_PATH = os.path.expanduser("~")
APP_PATH = os.path.join(HOME_PATH, ".rymtracks")
NLTK_PATH = os.path.join(APP_PATH, "nltk")

ENCODING = locale.getpreferredencoding().lower()
VERSION = "RYMTracks {}".format(
    ".".join(str(number) for number in __version__)
)


###############################################################################


def print_service_locations():
    """
    Just prints recognizible network locations.
    """

    for key in Service.network_locations():
        print(key)


def update_languages():
    """
    Updates NLTK data in your local home. Does nothing on Python 3 because
    NLTK does not support it yet.
    """

    shutil.rmtree(NLTK_PATH, True)
    os.makedirs(NLTK_PATH)

    for data in ("stopwords", "punkt", "maxent_treebank_pos_tagger"):
        nltk.download(data, download_dir=NLTK_PATH)


def encode(text):
    return six.text_type(text, ENCODING)


def main():
    """
    Main function. rymtracks script executes this.
    """

    opts = docopt.docopt( __doc__, version=VERSION)

    locations = list(six.moves.map(encode, opts["<location>"]))
    if opts["-f"]:
        with open(opts["-f"], "r") as res:
            locations.extend(six.moves.map(encode, res))

    if opts["-l"]:
        return print_service_locations()

    if opts["--update-languages"]:
        return update_languages()

    try:
        capitalize_init(NLTK_PATH)
    except LookupError:
        print("Language data is absent or corrupted.")
        try:
            input = raw_input("Do you want to update it? [Y/N]: ")
        except (EOFError, KeyboardInterrupt):
            print("")
            return

        try:
            input = distutils.util.strtobool(input)
        except ValueError:
            input = False

        if input:
            update_languages()
        else:
            print("It is ok, but capitalization would be pretty primitive")

    console(execute(locations))


##############################################################################


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
