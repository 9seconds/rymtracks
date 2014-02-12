# -*- coding: utf-8 -*-
"""
This module contains Service implementations of 7Digital.
http://7digital.com
"""


from ..base import SchemaOrgService


##############################################################################


class SevenDigital(SchemaOrgService):
    """
    Implementation of Service which is intended to parse 7Digital.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://schema.org/MusicRecording",
            itemprop="tracks"
        )

    def fetch_name(self, container):
        return container.find(itemprop="name")["content"]
