# -*- coding: utf-8 -*-
"""
This module contains Service implementation of BeatPort.
http://beatport.com
"""


from . import Service, HTMLMixin

from six import text_type


##############################################################################


class BeatPort(HTMLMixin, Service):
    """
    Implementation of Service which is intended to parse BeatPort.
    """

    def fetch_tracks(self, soup):
        return soup.select("table.track-grid tr.track-grid-content")

    def fetch_name(self, soup, container):
        column = container.find("td", class_="titleColumn")
        elements = column.find("a", class_="txt-larger").find_all("span")
        return " ".join(text_type(elem) for elem in elements)

    def fetch_track_length(self, soup, container):
        element = container.find_all("td")[-2].span
        return text_type(element).split("/")[0].strip()
