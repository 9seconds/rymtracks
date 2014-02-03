#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for iTunes service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class ITunesCase(FetchMixin, TestCase):
    """
    iTunes test case.
    """

    URL = "https://itunes.apple.com/ru/album/metamorphosis/id786140260"
    DATA = (
        (u("Siberia"), "5:28"),
        (u("Owl Path"), "5:36"),
        (u("Jackdaw Talk"), "3:42"),
        (u("September 13"), "4:52"),
        (u("Theory  Practice"), "3:36"),
        (u("Love Forever Krist"), "3:46"),
        (u("King Pony"), "2:41"),
        (u("September 23"), "6:11"),
        (u("Swan Path"), "4:52"),
        (u("Father"), "6:47")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
