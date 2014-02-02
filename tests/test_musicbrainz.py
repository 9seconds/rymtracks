#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for MusicBrainz service.
"""


from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class MusicBrainzCase(FetchMixin, TestCase):
    """
    MusicBrainz test case.
    """

    URL = "http://musicbrainz.org/release/" \
          "28a788fd-d6ca-46a8-8443-6403802c40e8"
    DATA = (
        (u("Look... The Sun Is Rising"), "5:12"),
        (u("Be Free, a Way"), "5:13"),
        (u("Try to Explain"), "5:00"),
        (u("You Lust"), "13:03"),
        (u("The Terror"), "6:22"),
        (u("You Are Alone"), "3:47"),
        (u("Butterfly, How Long It Takes to Die"), "7:31"),
        (u("Turning Violent"), "4:16"),
        (u("Always There, in Our Hearts"), "4:35"),
        (u("Sun Blows Up Today"), "3:10"),
        (u("All You Need Is Love"), "5:06")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)