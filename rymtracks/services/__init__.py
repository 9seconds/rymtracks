# -*- coding: utf-8 -*-
"""
Core logic of RYMTracks. Actually there are some functions which uses
Tornado IO loop and invokes parsers.
"""


from collections import OrderedDict, namedtuple
from itertools import chain
from re import compile as regex_compile
from urlparse import urlparse

from bs4 import BeautifulSoup
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.gen import coroutine, Return

try:
    # https://pypi.python.org/pypi/ujson
    from ujson import load as json_load
except ImportError:
    try:
        # http://simplejson.readthedocs.org. Since it is wide-spread I am sure
        # you have it
        from simplejson import load as json_load
    except ImportError:
        from json import load as json_load


##############################################################################


__all__ = "Service"

# Response structure for parsed results. exception is None if nothing happened
ParserResponse = namedtuple("ParserResponse", ["url", "data", "exception"])


##############################################################################


class HTMLMixin(object):

    @staticmethod
    def convert_response(response):
        return BeautifulSoup(response.buffer, "html")


class JSONMixin(object):

    @staticmethod
    def convert_response(response):
        return json_load(response.buffer)


class XMLMixin(object):

    @staticmethod
    def convert_response(response):
        return BeautifulSoup(response.buffer, "xml")


##############################################################################


class Service(object):

    _PARSERS = OrderedDict()

    # Regular expression to remove first zeroes properly
    ZERO_REGEXP = regex_compile(r"^0+(\d):")

    @classmethod
    def normalize_track_length(cls, length):
        return cls.ZERO_REGEXP.sub(r"\1:", length)

    @classmethod
    def register(cls, class_, *netlocs):
        cls._PARSERS = OrderedDict(
            chain(
                cls._PARSERS.iteritems(),
                ((loc, class_) for loc in netlocs)
            )
        )

    @classmethod
    def produce(cls, url, worker_pool):
        parsed_url = urlparse(url)
        for loc in cls._PARSERS:
            if parsed_url.netloc.endswith(loc):
                return cls._PARSERS[loc](url, worker_pool)

    @classmethod
    def network_locations(cls):
        return sorted(cls._PARSERS)

    def __init__(self, url, worker_pool):
        self.url = url
        self.worker_pool = worker_pool

    @coroutine
    def get_task(self):
        raw_response = yield AsyncHTTPClient().fetch(self.generate_request())
        future = self.worker_pool.submit(self.parse, raw_response)
        if future.exception():
            response = ParserResponse(self.url, [], future.exception())
        else:
            response = ParserResponse(self.url, future.result(), None)
        raise Return(response)

    def generate_request(self):
        return HTTPRequest(
            url=self.url,
            use_gzip=True,
            user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) "
                       "Gecko/20100101 Firefox/29.0"
        )

    def parse(self, response):
        converted_response = self.convert_response(response)
        tracks = self.fetch_tracks(converted_response)
        if not tracks:
            raise Exception("Empty list")
        extracted_data = []
        for container in tracks:
            extracted_data.append(
                (
                    self.fetch_name(converted_response, container),
                    self.fetch_time(converted_response, container)
                )
            )
        return tuple(extracted_data)

    def fetch_tracks(self, response):
        raise NotImplementedError("Not implemented in base class")

    def fetch_name(self, response, container):
        raise NotImplementedError("Not implemented in base class")

    def fetch_time(self, response, container):
        raise NotImplementedError("Not implemented in base class")


from .bandcamp import BandCamp
from .discogs import Discogs
from .rateyourmusic import RateYourMusic
from .musicbrainz import MusicBrainz
from .amazon import Amazon
from .itunes import ITunes
from .allmusic import AllMusic

Service.register(BandCamp, "bandcamp.com")
Service.register(Discogs, "discogs.com")
Service.register(RateYourMusic, "rateyourmusic.com")
Service.register(MusicBrainz, "musicbrainz.org")
Service.register(Amazon, "amazon.com", "amazon.co.uk", "amazon.co.jp")
Service.register(ITunes, "itunes.apple.com")
Service.register(AllMusic, "allmusic.com")
