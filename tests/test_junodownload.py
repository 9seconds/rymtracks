#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for JunoDownload service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from unittest import TestCase, main

from six import u


##############################################################################


class JunoDownload(FetchMixin, TestCase):
    """
    JunoDownload test case.
    """

    URL = "http://www.junodownload.com/products" \
          "/anton-maskeliade-one-beat/2401131-02/"
    DATA = (
        (u("Come on (Feat 1beat)"), "4:01"),
        (u("Circus (Feat Usman Riaz / Chance Mccoy / Song Hee Kwon)"), "4:02"),
        (u("Same (Feat Usman Riaz)"), "2:58")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)
