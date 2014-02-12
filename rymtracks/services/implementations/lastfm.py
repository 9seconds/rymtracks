# -*- coding: utf-8 -*-
"""
This module contains Service implementations of Last.fm.
http://last.fm
"""


from ..base import SchemaOrgService


##############################################################################


class LastFM(SchemaOrgService):
    """
    Implementation of Service which is intended to parse LastFM.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://schema.org/MusicRecording",
            itemprop="tracks"
        )

    def fetch_track_length(self, container):
        return container.find("td", class_="durationCell")
