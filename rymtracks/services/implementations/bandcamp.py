# -*- coding: utf-8 -*-
"""
This module contains Service implementations of BandCamp.
http://bandcamp.com
"""


from __future__ import absolute_import, unicode_literals

from ..schemaorg_service import SchemaOrgService


class BandCamp(SchemaOrgService):
    """
    Implementation of Service which is intended to parse BandCamp.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://www.schema.org/MusicRecording",
            itemprop="tracks"
        )

    def fetch_track_length(self, container):
        return container.find("span", class_="time")
