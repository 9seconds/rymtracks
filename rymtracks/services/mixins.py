# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import bs4

from .water import Water


class HTMLMixin(object):
    """
    Mixin which asserts that response contains HTML and converts it into
    Beautiful Soup instance.
    """

    @staticmethod
    def convert_response(response):
        """
        Converter of response into Beautiful Soup instance.
        """

        return Water(bs4.BeautifulSoup(response.text, "html"))


class JSONMixin(object):
    """
    Mixin which asserts that response contains JSON and parses it.
    """

    @staticmethod
    def convert_response(response):
        """
        Converts response into Python objects.
        """

        return response.json()


class XMLMixin(object):
    """
    Mixin which asserts that response contains XML and converts it into
    Beautiful Soup instance.
    """

    @staticmethod
    def convert_response(response):
        """
        Converter of response into Beautiful Soup instance.
        """

        return Water(bs4.BeautifulSoup(response.text, "xml"))