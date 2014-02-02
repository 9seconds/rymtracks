# -*- coding: utf-8 -*-
"""
This module contains Service implementation of BandCamp.
http://bandcamp.com
"""


from . import Service, HTMLMixin


##############################################################################


class BandCamp(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse Amazon MP3 Store.
    """

    def fetch_tracks(self, soup):
        return soup.select("#track_table div.title")

    def fetch_name(self, soup, container):
        return container.find("span", itemprop="name")

    def fetch_track_length(self, soup, container):
        return container.find("span", class_="time")
