# -*- coding: utf-8 -*-
"""
Services package. This module contains definitions of useful mixins and
main service class.
"""


from __future__ import division

from collections import namedtuple

from bs4 import BeautifulSoup
from isodate import parse_duration, ISO8601Error
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.gen import coroutine, Return
from six import u, text_type, string_types, callable as six_callable, Iterator
from six.moves.urllib.parse import urlparse

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


__all__ = "Service", "HTMLMixin", "JSONMixin", "XMLMixin"

# Response structure for parsed results. exception is None if nothing happened
ParserResponse = namedtuple("ParserResponse", ["url", "data", "exception"])


##############################################################################


class Water(Iterator):
    """
    Just simple wrapper around BeautifulSoup to avoid "if"-mess.
    """

    __slots__ = "_soup",

    # ------------------------------------------------------------------------

    def __init__(self, soup):
        self._soup = soup

    def __nonzero__(self):
        return bool(self._soup) if self._soup else False

    def __instancecheck__(self, instance):
        return isinstance(instance, getattr(self._soup, "__class__", None))

    def __len__(self):
        return len(self._soup) if self._soup else 0

    def __getitem__(self, key):
        return Water(self._soup[key]) if self._soup else self

    def __setitem__(self, key, value):
        if self._soup:
            self._soup[key] = value

    def __delitem__(self, key):
        if self._soup:
            del self._soup[key]

    def __iter__(self):
        return Water(iter(self._soup)) if self._soup else iter([])

    def __contains__(self, key):
        return key in self._soup if self._soup else False

    def __getslice__(self, i, j):
        return Water(self._soup[i:j]) if self._soup else Water([])

    def __getattr__(self, item):
        if hasattr(self._soup, item):
            return Water(getattr(self._soup, item))
        return self

    def __call__(self, *args, **kwargs):
        if six_callable(self._soup):
            return Water(self._soup(*args, **kwargs))
        return self

    def __str__(self):
        if self._soup:
            text = self._soup
            if not isinstance(self._soup, string_types):
                text = self._soup.get_text()
            return text_type(text.strip())
        else:
            return text_type("")

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return repr(self._soup)

    def __next__(self):
        return Water(next(self._soup))


##############################################################################


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
        return Water(BeautifulSoup(response.buffer, "html"))


class JSONMixin(object):
    """
    Mixin which asserts that response contains JSON and parses it.
    """

    @staticmethod
    def convert_response(response):
        """
        Converts response into Python objects.
        """
        return json_load(response.buffer)


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
        return Water(BeautifulSoup(response.buffer, "xml"))


##############################################################################


class ServiceFactoryMixin(object):
    """
    Service mixin provides interface for registering Service instances,
    factory method to produce instances according to URL etc.
    """

    # A collection of parser classes binded to network locations.
    _PARSERS = []

    # ------------------------------------------------------------------------

    @classmethod
    def register(cls, class_, *netlocs):
        """
        Registers parser class to the list of network locations. Please
        remember that lookup is done by longest name so if you want
        """
        cls._PARSERS += [(loc, class_) for loc in netlocs]
        cls._PARSERS.sort(key=lambda el: len(el[0]), reverse=True)

    @classmethod
    def produce(cls, url, worker_pool):
        """
        Factory method to return appropriate Service instance for given URL.
        """
        parsed_url = urlparse(url)
        for loc, class_ in cls._PARSERS:
            if parsed_url.netloc.endswith(loc):
                return class_(url, worker_pool)

    @classmethod
    def network_locations(cls):
        """
        Returns the list of parseable network locations.
        """
        return sorted(loc for loc, class_ in cls._PARSERS)


class Service(ServiceFactoryMixin):
    """
    Main service class contains almost all logic of service handling.

    It fetches data by URL, parses it and generates ParserResponse result.

    Main method to invoke is get_task which is suitable to run in Tornado
    IOLoop. It is actually coroutine which raises result. It invokes internal
    methods in following order:

        1. generate_request
        2. parse
        3. convert_response
        4. fetch_tracks
        5. fetch_name
        6. fetch_time

    Please check documentation on methods to realise what do you need to
    override to reach the goal.
    """

    USER_AGENT = u(
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) "
        "Gecko/20100101 Firefox/29.0"
    )

    # ------------------------------------------------------------------------

    @staticmethod
    def normalize_track_length(length):
        """
        Removes padded zeroes from time. In other words it converts length
        into RYM-approved form: 00:13 -> 0:13, 00:03 -> 0:03
        """
        if not length:
            return ""
        chunks = [int(chunk) for chunk in length.split(":")]
        while chunks[0] == 0:
            chunks = chunks[1:]
        if len(chunks) == 1:
            chunks = [0] + chunks
        chunks = [str(chunk) for chunk in chunks]
        chunks[1:] = [chunk.zfill(2) for chunk in chunks[1:]]
        return ":".join(chunks)

    @staticmethod
    def second_to_timestamp(seconds):
        """
        Converts seconds into text timestamp in RYM-approved format.
        """
        parts = []
        seconds = abs(seconds)
        while seconds:
            parts.append(seconds % 60)
            seconds //= 60

        if not parts:
            return ""
        if len(parts) == 1:
            parts[0:0] = [0]

        parts = [str(part) for part in reversed(parts)]
        parts[1:] = [part.zfill(2) for part in parts[1:]]
        return ":".join(parts)

    # ------------------------------------------------------------------------

    def __init__(self, url, worker_pool):
        """
        Constructor.

        url is url to fetch and worker_pool is  concurrent.futures-compatible
        worker pool to process fetched data.
        """
        self.url = url
        self.worker_pool = worker_pool

    # ------------------------------------------------------------------------

    @coroutine
    def get_task(self):
        """
        Main interface method user has to invoke. It returns Tornado future
        which you have to yield to Tornado IOLoop to get the ParserResponse
        result.
        """
        raw_response = yield AsyncHTTPClient().fetch(self.generate_request())
        future = self.worker_pool.submit(self.parse, raw_response)
        if future.exception():
            response = ParserResponse(self.url, [], future.exception())
        else:
            response = ParserResponse(self.url, future.result(), None)
        raise Return(response)

    def generate_request(self):
        """
        Generates request for Tornado AsyncHTTPClient. We have to use this
        method because you might want to rewrite URL (check MusicBrainz)
        and add custom User-Agent (hello Discogs!).
        """
        return HTTPRequest(
            self.url, use_gzip=True, user_agent=self.USER_AGENT
        )

    def parse(self, response):
        """
        The most common page parsing operation. First it converts result
        into parsed object instance and after that travers it. Actually
        it has to return some properly sorted tuple with pairs of name
        and track length.
        """
        converted_response = self.convert_response(response)
        tracks = self.fetch_tracks(converted_response)
        if not tracks:
            raise Exception("Empty list")
        extracted_data = []
        for container in tracks:
            title = str(self.fetch_name(converted_response, container))
            time = str(self.fetch_track_length(converted_response, container))
            time = self.normalize_track_length(time)
            extracted_data.append((title, time))
        return tuple(extracted_data)

    # ------------------------------------------------------------------------

    @staticmethod
    def convert_response(response):
        """
        Converts raw Tornado HTTPResponse into something meaningful.
        """
        return u(response.body)

    def fetch_tracks(self, response):
        """
        Fetches track containers from converted response.
        """
        raise NotImplementedError("Not implemented in base class")

    def fetch_name(self, response, container):
        """
        Fetches track name from track container.
        """
        raise NotImplementedError("Not implemented in base class")

    def fetch_track_length(self, response, container):
        """
        Fetches track length from track container.
        """
        raise NotImplementedError("Not implemented in base class")


class SchemaOrgService(HTMLMixin, Service):
    """
    Base service implementation to parse services which supports
    MusicRecording schema.

    http://schema.org/MusicRecording
    """

    def fetch_tracks(self, soup):
        return soup.find_all(
            itemtype="http://schema.org/MusicRecording",
            itemprop="track"
        )

    def fetch_name(self, soup, container):
        return container.find(itemprop="name")

    def fetch_track_length(self, soup, container):
        iso = str(container.find(itemprop="duration")["content"])
        try:
            return self.second_to_timestamp(parse_duration(iso).seconds)
        except ISO8601Error:
            return ""


##############################################################################


# Registering services
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
