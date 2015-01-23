# -*- coding: utf-8 -*-
"""
This module contains Service implementations of Archive.org.
http://archive.org
"""


from __future__ import absolute_import, unicode_literals

import requests
import six

from ..mixins import JSONMixin
from ..webservice import WebService
from ...capitalization import capitalize


class ArchiveOrg(JSONMixin, WebService):
    """
    Implementation of Service which is intended to parse Archive.org.
    """

    def generate_request(self):
        resource = self.location.rstrip("/").rpartition("/")[-1]
        return requests.Request(
            "GET", "http://archive.org/metadata/" + resource + "/files/",
            headers={
                "User-Agent": self.USER_AGENT,
                "Accept": "application/json"
            }
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
            title = capitalize(file_["title"])
            length = six.text_type(file_.get("length", ""))

            if length and ":" not in length:
                length = int(float(length))
                length = self.second_to_timestamp(length)

            length = self.normalize_track_length(length)
            tracks[track] = (title, length)

        if not tracks:
            raise Exception("Empty list")

        return tuple(data for track, data in sorted(six.iteritems(tracks)))
