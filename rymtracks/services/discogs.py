# -*- coding: utf-8 -*-
"""
This module contains Service implementation of Discogs.
http://discogs.com
"""


from . import Service, HTMLMixin


##############################################################################


class Discogs(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse Discogs.
    """

    def fetch_tracks(self, soup):
        return soup.select("#playlist- tr")

    def fetch_name(self, soup, container):
        return container.find("span", class_="track_title")

    def fetch_track_length(self, soup, container):
        return container.find("td", class_="track_duration").span
