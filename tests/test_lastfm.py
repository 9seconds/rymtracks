#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for LastFM service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class LastFMCase (FetchMixin, TestCase):
    """
    LastFM test case.
    """

    URL = "http://www.lastfm.ru/music/The+Chemical+Brothers/Surrender"
    DATA = (
        (u("Music : Response"), "5:20"),
        (u("Under The Influence"), "4:16"),
        (u("Out Of Control"), "7:21"),
        (u("Orange Wedge"), "3:06"),
        (u("Let Forever Be"), "3:56"),
        (u("The Sunshine Underground"), "8:38"),
        (u("Asleep From Day"), "4:47"),
        (u("Got Glint?"), "5:26"),
        (u("Hey Boy Hey Girl"), "4:50"),
        (u("Surrender"), "4:30"),
        (u("Dream On (Contains Hidden Track 'Dream On (Reprise)')"), "6:46")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
