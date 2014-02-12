# -*- coding: utf-8 -*-
"""
This module contains Service implementations of Amazon MP3 store.
http://amazon.com
"""


from ..base import HTMLMixin, WebService

from re import compile as regex_compile


##############################################################################


class Amazon(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse Amazon MP3 Store.
    """

    # This regexp is intended to remove leading track numbers from titles.
    LEADING_NUMBER = regex_compile(r"^\d+\.\s*")

    # ------------------------------------------------------------------------

    def fetch_tracks(self, soup):
        table = soup.select("#albumTrackList > table")[1].table
        return table.find_all("tr")[1:-1]

    def fetch_name(self, container):
        name = container.find("td", class_="titleCol")
        return self.LEADING_NUMBER.sub("", str(name))

    def fetch_track_length(self, container):
        return container.find("td", class_="runtimeCol")
