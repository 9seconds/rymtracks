# -*- coding: utf-8 -*-
"""
This module contains Service implementations of MusicBrainz.
http://musicbrainz.org
"""


from __future__ import division

from ..base import XMLMixin, WebService

from requests import Request
from six import text_type
from six.moves.urllib.parse import urlparse


##############################################################################


class MusicBrainz(XMLMixin, WebService):
    """
    Implementation of Service which is intended to parse MusicBrainz.
    """

    def generate_request(self):
        url = urlparse(self.location).path.rstrip("/").rpartition("/")[-1]
        url = "http://musicbrainz.org/ws/2/release/" + url
        return Request(
            'GET', url,
            params={
                "inc": "recordings"
            },
            headers={
                "User-Agent": self.USER_AGENT
            }
        )

    def fetch_tracks(self, soup):
        return soup.find_all("track")

    def fetch_name(self, container):
        return container.find("recording").title

    def fetch_track_length(self, container):
        time = container.find("length")
        if not time:
            return ""
        # text_type is a must here because we have to convert Water
        # to text first.
        return self.second_to_timestamp(int(text_type(time)) // 1000)
