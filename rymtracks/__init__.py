#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RYMTracks scraps given URLs and presents tracklists into copypasteable form
for RateYourMusic.com.

Usage:
    rymtracks <url>...
    rymtracks -f <filename>
    rymtracks -l
    rymtracks (-h | --help)
    rymtracks --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -f            Filename with urls.
    -l            Show parseable network locations.
"""


from .core import execute
from .formatters import console
from .services import Service

from sys import exit as sysexit

from docopt import docopt
from six import print_


##############################################################################


__version__ = 0, 1, 0
__all__ = 'main',


##############################################################################


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
    urls = [str(url) for url in opts["<url>"]]
    if opts["-l"]:
        for key in Service.network_locations():
            print_(key)
        return
    if opts["<filename>"]:
        with open(opts["<filename>"], "r") as res:
            urls.extend(str(url) for url in res.readlines())
    console(execute(urls))


##############################################################################


if __name__ == "__main__":
    sysexit(main())
