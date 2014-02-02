#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for RateyourMusic service.
"""


from unittest import TestCase, main

from mixins import FetchMixin


##############################################################################


class RateYourMusicCase (FetchMixin, TestCase):
    """
    Amazon test case.
    """

    URL = "https://rateyourmusic.com/release/album/linkin_park/meteora/"
    DATA = (
        (u'Foreword', '13:00'),
        (u"Don't Stay", '3:07'),
        (u'Somewhere I Belong', '3:33'),
        (u'Lying From You', '2:55'),
        (u'Hit the Floor', '2:44'),
        (u'Easier to Run', '3:24'),
        (u'Faint', '2:42'),
        (u'Figure.09', '3:17'),
        (u'Breaking the Habit', '3:16'),
        (u'From the Inside', '2:53'),
        (u"Nobody's Listening", '2:58'),
        (u'Session', '2:23'),
        (u'Numb', '3:05'),
        (u'Bonus Materials - Enhanced', ''),
        (u'"The Art of Meteora"', ''),
        (u'Website Toolkit', ''),
        (u'Exclusive Access to Web-based Media', '')
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)