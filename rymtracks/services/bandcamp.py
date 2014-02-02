# -*- coding: utf-8 -*-
"""
This module contains Service implementation of BandCamp.
http://bandcamp.com
"""


from . import SchemaOrgService


##############################################################################


class BandCamp(SchemaOrgService):
    """
    Implementation of Service which is intended to parse BandCamp.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://www.schema.org/MusicRecording",
            itemprop="tracks"
        )

    def fetch_track_length(self, soup, container):
        return container.find("span", class_="time")
