#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for BandCamp service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class BandCampCase(FetchMixin, TestCase):
    """
    BandCamp test case.
    """

    URL = "http://aidanbaker.bandcamp.com/album/cameo"
    DATA = (
        (u("Cameo 1"), "21:00"),
        (u("Cameo Interlude"), "8:46"),
        (u("Cameo 2"), "18:56")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
