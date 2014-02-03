#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Boomkat service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class BoomkatCase(FetchMixin, TestCase):
    """
    Boomkat test case.
    """

    URL = "http://boomkat.com/downloads/" \
          "463786-peter-broderick-music-for-confluence"
    DATA = (
        (u("In The Valley Itself"), "2:58"),
        (u("The Last Christmas"), "1:44"),
        (u("We Didn't Find Anything"), "2:03"),
        (u("Some Fisherman On The Snake River"), "4:25"),
        (u("We Enjoyed Life Together"), "1:46"),
        (u("She Just Quit Coming To School"), "2:07"),
        (u("It Wasn't A Deer Skull"), "3:04"),
        (u("What Was Found"), "2:16"),
        (u("He Was Inside That Building"), "6:41"),
        (u("The Person Of Interest"), "5:27"),
        (u("Circumstantial Evidence"), "3:24"),
        (u("Until The Person Is Aprehended"), "6:50"),
        (u("Old Time"), "3:24")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)