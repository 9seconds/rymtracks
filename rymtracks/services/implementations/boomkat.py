# -*- coding: utf-8 -*-
"""
This module contains Service implementations of Boomkat.
http://boomkat.com
"""


from ..base import HTMLMixin, WebService

from re import compile as regex_compile

from six import text_type


##############################################################################


class Boomkat(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse Boomkat.
    """

    # This regexp is intended to remove leading track numbers from titles.
    LEADING_NUMBER = regex_compile(r"^\d+\.\s*")

    def fetch_tracks(self, soup):
        return soup.select("#tracks-background-top div.tracks-listing")

    def fetch_name(self, container):
        title = container.find("div", class_="track-listing-title")
        title.span.decompose()
        title = text_type(title)
        title = self.LEADING_NUMBER.sub("", title)
        title = title.lstrip(": ").rstrip()
        return title

    def fetch_track_length(self, container):
        return container.find("div", class_="track-listing-duration ")
