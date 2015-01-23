# -*- coding: utf-8 -*-
"""
This module contains Service implementations of ProgArchives.
http://progarchives.com
"""


from __future__ import absolute_import, unicode_literals

import re

import six

from ..mixins import HTMLMixin
from ..webservice import WebService
from ...capitalization import capitalize


class ProgArchives(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse ProgArchives.
    """

    TRACK_REGEXP = re.compile(
        r"""
            ^
            (?P<number>\d+)\.\s*
            (?P<title>.*?)\s*
            (?:
                \(
                    (?P<length>(?:\d+:)*\d+)
                \)
            )?\s*
            $
        """,
        re.VERBOSE
    )

    def parse(self, response):
        converted_response = self.convert_response(response)

        tracks = converted_response.table.find_all("td")
        tracks = tracks[-1].p
        tracks = [
            six.text_type(chunk).strip() for chunk in tracks.stripped_strings
        ]

        extracted_data = []
        for track in tracks:
            matcher = self.TRACK_REGEXP.search(track)
            if not matcher:
                continue

            matches = matcher.groupdict()
            title = capitalize(matches["title"])
            length = self.normalize_track_length(matches["length"] or "")
            extracted_data.append((title, length))

        if not extracted_data:
            raise Exception("Empty list")

        return tuple(extracted_data)
