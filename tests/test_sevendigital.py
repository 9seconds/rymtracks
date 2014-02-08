#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for 7Digital service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class SevenDigitalCase(FetchMixin, TestCase):
    """
    7Digital test case.
    """

    URL = "http://www.7digital.com/artist/maximo-park-1/release/" \
          "too-much-information"
    DATA = (
        (u("Give, Get, Take"), "3:20"),
        (u("Brain Cells"), "3:09"),
        (u("Leave This Island"), "4:01"),
        (u("Lydia, the Ink Will Never Dry"), "3:02"),
        (u("My Bloody Mind"), "3:42"),
        (u("Is It True?"), "3:47"),
        (u("Drinking Martinis"), "3:31"),
        (u("I Recognise the Light"), "2:16"),
        (u("Midnight on the Hill"), "4:06"),
        (u("Her Name Was Audre"), "2:00"),
        (u("Where We're Going"), "2:45")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
