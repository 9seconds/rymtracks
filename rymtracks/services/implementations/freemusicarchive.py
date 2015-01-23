# -*- coding: utf-8 -*-
"""
This module contains Service implementations of FreeMusicArchive.
http://freemusicarchive.com
"""


from __future__ import absolute_import, unicode_literals

import six

from ..mixins import HTMLMixin
from ..webservice import WebService


class FreeMusicArchive(HTMLMixin, WebService):
    """
    Implementation of Service which is intended to parse FreeMusicArchive.
    """

    def fetch_tracks(self, soup):
        return soup.select("#content div.playlist div.play-item")

    def fetch_name(self, container):
        return container.find("span", class_="playtxt").a

    def fetch_track_length(self, container):
        length = container.find("span", class_="playtxt")
        length.a.decompose()
        length.b.decompose()
        return six.text_type(length).strip("() ")
