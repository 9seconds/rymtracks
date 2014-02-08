#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Jamendo service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class JamendoCase(FetchMixin, TestCase):
    """
    Jamendo test case.
    """

    URL = "http://www.jamendo.com/en/list/a128698/sue-o-de-dahlia"
    DATA = (
        (u("Entre Tu Y Yo Track"), "4:03"),
        (u("Creo En Ti"), "3:18"),
        (u("De Que Vale"), "3:33"),
        (u("Inyecci\xf3n De Vida"), "3:45"),
        (u("Marioneta"), "3:28"),
        (u("Quedate"), "3:24"),
        (u("Una Oportunidad"), "3:50"),
        (u("Encanto Natural"), "3:42"),
        (u("Marioneta Acustico"), "3:39"),
        (u("Entre Tu Y Yo Acustico"), "3:29")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
