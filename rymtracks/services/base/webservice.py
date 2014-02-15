# -*- coding: utf-8 -*-


from .service import Service, ParserResponse
from .mixins import HTMLMixin
from ...capitalization import capitalize

from isodate import parse_duration, ISO8601Error
from six import u, text_type
from requests import Session, Request


###############################################################################


class WebService(Service):

    USER_AGENT = u(
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) "
        "Gecko/20100101 Firefox/29.0"
    )

    # ------------------------------------------------------------------------

    def __init__(self, location):
        super(WebService, self).__init__(location)
        self.session = Session()

    # ------------------------------------------------------------------------

    def get_result(self):
        response = self.session.send(
            self.generate_request().prepare(),
            timeout=60.0,
            stream=False,
            verify=False
        )
        response.raise_for_status()

        try:
            parsed_result = self.parse(response)
        except Exception as exc:
            return ParserResponse(self.location, [], exc)
        return ParserResponse(self.location, parsed_result, None)

    def generate_request(self):
        return Request(
            "GET", self.location,
            headers={
                "User-Agent": self.USER_AGENT,
            }
        )

    def parse(self, response):
        converted_response = self.convert_response(response)
        tracks = self.fetch_tracks(converted_response)
        if not tracks:
            raise Exception("Empty list")
        extracted_data = []
        for container in tracks:
            title = self.fetch_name(container)
            title = capitalize(title)
            time = self.fetch_track_length(container)
            time = self.normalize_track_length(text_type(time))
            extracted_data.append((title, time))
        return tuple(extracted_data)

    # ------------------------------------------------------------------------

    @staticmethod
    def convert_response(response):
        return response.text

    def fetch_tracks(self, response):
        return []

    def fetch_name(self, container):
        return ""

    def fetch_track_length(self, container):
        return ""


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
        iso = text_type(container.find(itemprop="duration")["content"])
        try:
            return self.second_to_timestamp(parse_duration(iso).seconds)
        except ISO8601Error:
            return ""