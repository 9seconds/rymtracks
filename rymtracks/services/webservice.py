# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

import requests
import six

from .service import Service, ParserResponse
from ..capitalization import capitalize


class WebService(Service):

    USER_AGENT = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) "
        "Gecko/20100101 Firefox/29.0"
    )
    SEND_ATTEMPTS = 3
    SEND_PARAMS = {
        "timeout": 10,
        "stream": False
    }

    def __init__(self, location):
        super(WebService, self).__init__(location)

        self.session = requests.Session()

    def get_result(self):
        try:
            response = self.try_to_send(self.generate_request().prepare())
            response.raise_for_status()
        except requests.RequestException as exc:
            return ParserResponse(self.location, [], exc)

        try:
            parsed_result = self.parse(response)
        except Exception as exc:
            return ParserResponse(self.location, [], exc)
        return ParserResponse(self.location, parsed_result, None)

    def try_to_send(self, prepared_request):
        for attempt in xrange(self.SEND_ATTEMPTS - 1):
            try:
                return self.session.send(prepared_request, **self.SEND_PARAMS)
            except Exception:
                pass

        return self.session.send(prepared_request, **self.SEND_PARAMS)

    def generate_request(self):
        return requests.Request(
            "GET", self.location,
            headers={"User-Agent": self.USER_AGENT}
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
            time = self.normalize_track_length(six.text_type(time))
            extracted_data.append((title, time))

        return tuple(extracted_data)

    @staticmethod
    def convert_response(response):
        return response.text

    def fetch_tracks(self, response):
        return []

    def fetch_name(self, container):
        return ""

    def fetch_track_length(self, container):
        return ""
