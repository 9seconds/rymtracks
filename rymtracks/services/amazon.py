# -*- coding: utf-8 -*-
"""
This module contains Service implementation of Amazon MP3 store.
http://amazon.com
"""


from . import Service, HTMLMixin

from re import compile as regex_compile


##############################################################################


class Amazon(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse Amazon MP3 Store.
    """

    # This regexp is intended to remove leading track numbers from titles.
    LEADING_NUMBER = regex_compile(r"^\d+\.\s*")

    # ------------------------------------------------------------------------

    def fetch_tracks(self, soup):
        tables = soup.select("#albumTrackList > table")
        if tables:
            tables = tables[1].table
            if tables:
                return tables.find_all("tr")[1:-1]
        return []

    def fetch_name(self, soup, container):
        name = container.find("td", class_="titleCol")
        if not name:
            return ""
        return self.LEADING_NUMBER.sub("", name.get_text().strip())

    def fetch_track_length(self, soup, container):
        time = container.find("td", class_="runtimeCol") or ""
        if not time:
            return ""
        return self.normalize_track_length(time.get_text().strip())
