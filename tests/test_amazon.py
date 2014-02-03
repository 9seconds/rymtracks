#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for Amazon service.
"""


if __name__ == "__main__":
    from mixins import FetchMixin
else:
    from .mixins import FetchMixin

from six import u

from unittest import TestCase, main


##############################################################################


class AmazonCase (FetchMixin, TestCase):
    """
    Amazon test case.
    """

    URL = "http://www.amazon.co.uk/gp/product/B00B7PJM42"
    DATA = (
        (u("Look?The Sun Is Rising"), "5:11"),
        (u("Be Free, A Way"), "5:13"),
        (u("Try To Explain"), "5:00"),
        (u("You Lust [feat. Phantogram]"), "13:02"),
        (u("The Terror"), "6:21"),
        (u("You Are Alone"), "3:45"),
        (u("Butterfly, How Long It Takes To Die"), "7:30"),
        (u("Turning Violent"), "4:16"),
        (u("Always There, In Our Hearts"), "4:15")
    )


##############################################################################


if __name__ == "__main__":
    main(verbosity=2)