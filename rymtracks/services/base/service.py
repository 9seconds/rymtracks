# -*- coding: utf-8 -*-


from collections import namedtuple, OrderedDict

from six import text_type
from six.moves.urllib.parse import urlparse


###############################################################################


__all__ = "ParserResponse", "Service"


###############################################################################


# Response structure for parsed results. exception is None if nothing happened
ParserResponse = namedtuple(
    "ParserResponse", ["location", "data", "exception"]
)


###############################################################################


class Service(object):
    """
    Service mixin provides interface for registering Service instances,
    factory method to produce instances according to URL etc.
    """

    # A collection of parser classes binded to network locations.
    _PARSERS = OrderedDict()

    # -------------------------------------------------------------------------

    @classmethod
    def register(cls, class_, *locations):
        """
        Registers parser class to the list of network locations. Please
        remember that lookup is done by longest name so if you want
        """
        cls._PARSERS = OrderedDict(
            sorted(
                cls._PARSERS.items() + [(loc, class_) for loc in locations],
                key=lambda item: len(item[0]), reverse=True
            )
        )

    @classmethod
    def produce(cls, location):
        """
        Factory method to return appropriate Service instance for given URL.
        """
        if location.startswith(("http://", "https://")):
            parsed_url = urlparse(location)
            for loc, class_ in cls._PARSERS.iteritems():
                if parsed_url.netloc.endswith(loc):
                    return class_(location)
        else:
            from ..implementations import FILESYSTEM_LOCATION
            return cls._PARSERS[FILESYSTEM_LOCATION](location)

    @classmethod
    def network_locations(cls):
        """
        Returns the list of parseable network locations.
        """
        from ..implementations import FILESYSTEM_LOCATION
        return sorted(
            loc for loc, class_ in cls._PARSERS.iteritems()
            if loc != FILESYSTEM_LOCATION
        )

    # -------------------------------------------------------------------------

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
        chunks = [text_type(chunk) for chunk in chunks]
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

        parts = [text_type(part) for part in reversed(parts)]
        parts[1:] = [part.zfill(2) for part in parts[1:]]
        return ":".join(parts)

    # -------------------------------------------------------------------------

    def __init__(self, location):
        self.location = location

    # -------------------------------------------------------------------------

    def get_result(self):
        """
        Main interface method user has to invoke.
        """
        return ParserResponse(None, [], None)