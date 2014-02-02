# -*- coding: utf-8 -*-
"""
This module contains Service implementation of RateYourMusic.
http://rateyourmusic.com
"""


from . import Service, HTMLMixin


##############################################################################


class RateYourMusic(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse RateYourMusic.
    Yes, because I can.
    """

    def fetch_tracks(self, soup):
        return soup.select("#tracks div.tracklist_line")

    def fetch_name(self, soup, container):
        return container.find("span", itemprop="name")

    def fetch_track_length(self, soup, container):
        return container.find("span", itemprop="duration")
