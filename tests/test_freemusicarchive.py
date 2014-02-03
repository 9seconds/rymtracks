#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for FreeMusicArchive service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class FreeMusicArchiveCase(FetchMixin, TestCase):
    """
    FreeMusicArchive test case.
    """

    URL = "http://freemusicarchive.com/music/La_Desunion/My_God_is_a_Gun"
    DATA = (
        (u("The Undetected Sheep"), "4:33"),
        (u("Black Museum"), "7:14")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
