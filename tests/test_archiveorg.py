#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Archive.org service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class ArchiveOrgCase (FetchMixin, TestCase):
    """
    Archive.org test case.
    """

    URL = "https://archive.org/details/sute016"
    DATA = (
        (u("Komnata"), "4:59"),
        (u("It Seems"), "3:58"),
        (u("O Nei"), "3:46"),
        (u("For Pogisto"), "1:32"),
        (u("Let A"), "4:57"),
        (u("Fortnight"), "4:35"),
        (u("So Soft"), "4:15"),
        (u("Not A Big Deal"), "3:41"),
        (u("Long Time No See"), "3:57"),
        (u("Like A Wind"), "7:10"),
        (u("Owen"), "5:14")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
