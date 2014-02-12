# -*- coding: utf-8 -*-
"""
This module contains Service implementations of ProgArchives.
http://progarchives.com
"""


from ..base import HTMLMixin, WebService
from ...capitalization import capitalize

from re import compile as regex_compile, VERBOSE as regex_VERBOSE

from six import text_type


##############################################################################


class ProgArchives(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse ProgArchives.
    """

    TRACK_REGEXP = regex_compile(
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
        regex_VERBOSE
    )

    def parse(self, response):
        converted_response = self.convert_response(response)

        tracks = converted_response.table.find_all("td")
        tracks = tracks[-1].p
        tracks = [
            text_type(chunk).strip() for chunk in tracks.stripped_strings
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
