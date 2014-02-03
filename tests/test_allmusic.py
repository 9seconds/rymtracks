#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for AllMusic service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class AllMusicCase(FetchMixin, TestCase):
    """
    AllMusic test case.
    """

    URL = "http://www.allmusic.com/album/mw0000102770"
    DATA = (
        (u("Papercut"), "3:05"),
        (u("One Step Closer"), "2:36"),
        (u("With You"), "3:23"),
        (u("Points of Authority"), "3:20"),
        (u("Crawling"), "3:29"),
        (u("Runaway"), "3:04"),
        (u("By Myself"), "3:10"),
        (u("In the End"), "3:36"),
        (u("Place for My Head"), "3:05"),
        (u("Forgotten"), "3:14"),
        (u("Cure for the Itch"), "2:37"),
        (u("Pushing Me Away"), "3:12")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
