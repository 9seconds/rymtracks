#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Discogs service.
"""


from unittest import TestCase, main

from mixins import FetchMixin


##############################################################################


class DiscogsCase (FetchMixin, TestCase):
    """
    Amazon test case.
    """

    URL = "http://www.discogs.com/Radiohead-The-Bends/release/368116"
    DATA = (
        (u'Planet Telex', '4:18'),
        (u'The Bends', '4:06'),
        (u'High And Dry', '4:18'),
        (u'Fake Plastic Trees', '4:50'),
        (u'Bones', '3:09'),
        (u'(Nice Dream)', '3:53'),
        (u'Just', '3:55'),
        (u'My Iron Lung', '4:36'),
        (u'Bullet Proof..I Wish I Was', '3:29'),
        (u'Black Star', '4:07'),
        (u'Sulk', '3:43'),
        (u'Street Spirit (Fade Out)', '4:12')
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)