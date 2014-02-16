# -*- coding: utf-8 -*-
"""
Just a collections ot utilites used here and there.
"""


from contextlib import contextmanager
from functools import reduce as six_reduce

from colorama import Fore, Back, Style
from termcolor import colored as termcolored
from six import print_


###############################################################################


COLORED = True


###############################################################################


@contextmanager
def colored(*colorama_options):
    set_options = six_reduce(lambda x, y: x + y, colorama_options, "")
    print_(set_options, end="")

    yield

    print_(Fore.RESET + Back.RESET + Style.RESET_ALL, end="")


def msg(message, foreground=None, background=None, attrs=None):
    if not COLORED:
        return message
    return termcolored(message, foreground, background, attrs)