# -*- coding: utf-8 -*-
"""
This module contains Service implementations of JunoDownload.
http://junodownload.com
"""


from ..base import SchemaOrgService


##############################################################################


class JunoDownload(SchemaOrgService):
    """
    Implementation of Service which is intended to parse JunoDownload.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://schema.org/MusicRecording",
            itemprop="tracks"
        )

    def fetch_track_length(self, container):
        return container.find(
            "div",
            class_="product_tracklist_heading_records_length"
        )
