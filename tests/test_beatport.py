#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for BeatPort service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class BeatPort(FetchMixin, TestCase):
    """
    BeatPort test case.
    """

    URL = "http://www.beatport.com/release/baikal/1195150"
    DATA = (
        (u("Baikal Original Mix"), "4:57"),
        (u("Baikal Benji vaughan Remix"), "6:40"),
        (u("Baikal Tripswitch Space Mix"), "8:17"),
        (u("Baikal Electrosoul System Remix"), "8:47"),
        (u("Baikal Tripswitch Race Mix"), "8:51")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
