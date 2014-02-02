# -*- coding: utf-8 -*-
"""
This module contains Service implementation of MusicBrainz.
http://musicbrainz.org
"""


from . import Service, XMLMixin

from six.moves.urllib.parse import urlparse
from tornado.httpclient import HTTPRequest
from tornado.httputil import url_concat


##############################################################################


class MusicBrainz(XMLMixin, Service):
    """
    Implementation of Service which is intended to parse MusicBrainz.
    """

    def generate_request(self):
        url = urlparse(self.url).path.rstrip("/").rpartition("/")[-1]
        url = "http://musicbrainz.org/ws/2/release/" + url
        url = url_concat(url, dict(inc="recordings"))
        return HTTPRequest(url, use_gzip=True, user_agent=self.USER_AGENT)

    def fetch_tracks(self, soup):
        return soup.find_all("track")

    def fetch_name(self, soup, container):
        return container.find("recording").title

    def fetch_track_length(self, soup, container):
        time = container.find("length")
        if not time:
            return ""
        # str is a must here because we have to convert Water to text first.
        return self.second_to_timestamp(int(str(time)) // 1000)
