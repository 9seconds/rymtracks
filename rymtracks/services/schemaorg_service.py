# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import six
import isodate

from .mixins import HTMLMixin
from .webservice import WebService


class SchemaOrgService(HTMLMixin, WebService):
    """
    Base service implementations to parse services which supports
    MusicRecording schema.

    http://schema.org/MusicRecording
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://schema.org/MusicRecording",
            itemprop="track"
        )

    def fetch_name(self, container):
        return container.find(itemprop="name")

    def fetch_track_length(self, container):
        iso = six.text_type(container.find(itemprop="duration")["content"])
        try:
            return self.second_to_timestamp(isodate.parse_duration(iso).seconds)
        except isodate.ISO8601Error:
            return ""