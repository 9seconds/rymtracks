#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for ProgArchives service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from six import u

from unittest import TestCase, main


##############################################################################


class ProgArchivesCase(FetchMixin, TestCase):
    """
    ProgArchives test case.
    """

    URL = "http://www.progarchives.com/album.asp?id=42715"
    DATA = (
        (u("Immortal"), "4:15"),
        (u("Corners"), "7:57"),
        (u("Conformity Song"), "3:15"),
        (u("Dirty Secrets"), "4:56"),
        (u("I Don't Want to Know Today"), "4:20"),
        (u("Deadline"), "2:14"),
        (u("Divide"), "5:12"),
        (u("Hopes of Yesterday"), "5:59"),
        (u("Ascent"), "11:46")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
