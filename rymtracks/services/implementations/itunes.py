# -*- coding: utf-8 -*-
"""
This module contains Service implementations of iTunes.
http://itunes.apple.com
"""


from ..base import HTMLMixin, WebService


##############################################################################


class ITunes(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse iTunes.
    """

    def fetch_tracks(self, soup):
        tracks = soup.select(
            "div.track-list .tracklist-content-box > .tracklist-table"
        )
        return tracks[0].find_all("tr", class_="song")

    def fetch_name(self, container):
        return container.find("td", class_="name").find("span", class_="text")

    def fetch_track_length(self, container):
        return container.find("td", class_="time").find("span", class_="text")
