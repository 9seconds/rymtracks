# -*- coding: utf-8 -*-
"""
This module contains Service implementation of AllMusic Guide service.
http://allmusic.com
"""


from . import Service, HTMLMixin


##############################################################################


class AllMusic(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse AMG.
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            "tr",
            itemtype="http://schema.org/MusicRecording",
            itemprop="track"
        )

    def fetch_name(self, soup, container):
        name = container.find("div", itemprop="name")
        return name.get_text().strip() if name else ""

    def fetch_track_length(self, soup, container):
        time = container.find("td", class_="time")
        if not time:
            return ""
        return self.normalize_track_length(time.get_text().strip())
