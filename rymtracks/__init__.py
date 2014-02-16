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
    --no-color          Removes colored output
    -f                  Filename with urls.
    -l                  Show parseable network locations.

If you have any question please contact Sergey Arkhipov
(serge@aerialsounds.org) or use GitHub issue tracker:
https://github.com/9seconds/rymtracks/issues
"""


from .utils import colored, msg

from distutils.util import strtobool
from locale import getpreferredencoding
from os import makedirs
from os.path import exists, expanduser, join as path_join
from shutil import rmtree
from sys import exit as sysexit

from docopt import docopt
from colorama import init as colorama_init, Fore
from six import PY2, text_type, print_


###############################################################################


__version__ = 0, 1, 4
__all__ = 'main',


###############################################################################


HOME_PATH = path_join(expanduser("~"), ".rymtracks")
NLTK_PATH = path_join(HOME_PATH, "nltk")

ENCODING = getpreferredencoding().lower()

colorama_init()


###############################################################################


def print_service_locations():
    """
    Just prints recognizible network locations.
    """
    from .services import Service

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

    locations = [text_type(url, ENCODING) for url in opts["<location>"]]
    if opts["-f"]:
        with open(opts["-f"], "r") as res:
            locations.extend(
                text_type(url, ENCODING) for url in res.readlines()
            )
    if opts["--no-color"]:
        import utils
        utils.COLORED = False
    if opts["-l"]:
        return print_service_locations()
    if opts["--update-languages"]:
        return update_languages()

    if PY2:
        try:
            from .capitalization.py2 import capitalize
        except LookupError:
            print_(
                msg(
                    "Language data is absent or corrupted.",
                    "cyan"
                )
            )
            try:
                message = msg("Do you want to update it? ", "cyan")
                message += msg("[Y/N]", "cyan", attrs=["bold"])
                message += msg(": ", "cyan")
                input = raw_input(message)
            except (EOFError, KeyboardInterrupt):
                print_("")
                sysexit(0)
            try:
                input = strtobool(input)
            except ValueError:
                input = False

            if input:
                with colored(Fore.MAGENTA):
                    update_languages()
            else:
                print_(
                    msg(
                        "It is ok, but capitalization would "
                        "be pretty primitive",
                        "cyan"
                    )
                )

    from .core import execute
    from .formatters import console

    console(execute(locations))


##############################################################################


if __name__ == "__main__":
    try:
        sysexit(main())
    except KeyboardInterrupt:
        pass
