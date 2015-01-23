# -*- coding: utf-8 -*-
"""
This module contains Service implementations of Amazon MP3 store.
http://amazon.com
"""


from __future__ import absolute_import, unicode_literals

import re

from ..mixins import HTMLMixin
from ..webservice import WebService


class Amazon(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse Amazon MP3 Store.
    """

    # This regexp is intended to remove leading track numbers from titles.
    LEADING_NUMBER = re.compile(r"^\d+\.\s*")

    def fetch_tracks(self, soup):
        table = soup.select("#albumTrackList > table")[1].table
        return table.find_all("tr")[1:-1]

    def fetch_name(self, container):
        name = container.find("td", class_="titleCol")
        return self.LEADING_NUMBER.sub("", str(name))

    def fetch_track_length(self, container):
        return container.find("td", class_="runtimeCol")
