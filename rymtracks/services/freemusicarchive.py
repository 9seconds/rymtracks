# -*- coding: utf-8 -*-
"""
This module contains Service implementation of FreeMusicArchive.
http://freemusicarchive.com
"""


from . import Service, HTMLMixin

from six import text_type


##############################################################################


class FreeMusicArchive(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse FreeMusicArchive.
    """

    def fetch_tracks(self, soup):
        return soup.select("#content div.playlist div.play-item")

    def fetch_name(self, soup, container):
        return container.find("span", class_="playtxt").a

    def fetch_track_length(self, soup, container):
        length = container.find("span", class_="playtxt")
        length.a.decompose()
        length.b.decompose()
        return text_type(length).strip("() ")
