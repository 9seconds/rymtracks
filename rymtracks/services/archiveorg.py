# -*- coding: utf-8 -*-
"""
This module contains Service implementation of Archive.org.
http://archive.org
"""


from . import Service, JSONMixin

from six import text_type, iteritems
from tornado.httpclient import HTTPRequest


##############################################################################


class ArchiveOrg(JSONMixin, Service):
    """
    Implementation of Service which is intended to parse Archive.org.
    """

    def generate_request(self):
        resource = self.url.rstrip("/").rpartition("/")[-1]
        return HTTPRequest(
            "http://archive.org/metadata/" + resource + "/files/",
            use_gzip=True,
            headers=dict(Accept="application/json")
        )

    def parse(self, response):
        converted_response = self.convert_response(response)

        tracks = {}
        required_fields = ("title", "track", "album")
        for file_ in converted_response["result"]:
            if file_.get("source") != "original":
                continue
            if not all(field in file_ for field in required_fields):
                continue

            track = int(file_["track"])
            title = text_type(file_["title"])
            length = text_type(file_.get("length", ""))
            if length and ":" not in length:
                length = int(float(length))
                length = self.second_to_timestamp(length)
            length = self.normalize_track_length(length)
            tracks[track] = (title, length)

        if not tracks:
            raise Exception("Empty list")
        return tuple(data for track, data in sorted(iteritems(tracks)))
