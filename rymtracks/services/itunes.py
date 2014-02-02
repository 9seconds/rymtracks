# -*- coding: utf-8 -*-
"""
This module contains Service implementation of iTunes.
http://itunes.apple.com
"""


from . import Service, HTMLMixin


##############################################################################


class ITunes(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse iTunes.
    """

    def fetch_tracks(self, soup):
        tracks = soup.select(
            "div.track-list .tracklist-content-box > .tracklist-table"
        )
        if tracks:
            return tracks[0].select("tr.song")
        return []

    def fetch_name(self, soup, container):
        name = container.find("td", class_="name")
        if not name:
            return ""
        name = name.find("span", class_="text")
        return name.get_text().strip() if name else ""

    def fetch_track_length(self, soup, container):
        time = container.find("td", class_="time")
        if not time:
            return ""
        time = time.find("span", class_="text")
        if not time:
            return ""
        return self.normalize_track_length(time.get_text().strip())
