# -*- coding: utf-8 -*-


from . import Service, XMLMixin

from urlparse import urlparse

from tornado.httpclient import HTTPRequest
from tornado.httputil import url_concat


class MusicBrainz(XMLMixin, Service):

    def generate_request(self):
        url = urlparse(self.url).path.rstrip("/").rpartition("/")[-1]
        url = "http://musicbrainz.org/ws/2/release/" + url
        url = url_concat(url, dict(inc="recordings"))

        return HTTPRequest(
            url=url,
            use_gzip=True,
            user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) "
                       "Gecko/20100101 Firefox/29.0"
        )

    def fetch_tracks(self, soup):
        return soup.find_all("track")

    def fetch_name(self, soup, container):
        recording = container.find("recording")
        if not recording:
            return ""
        name = recording.title
        if not name:
            return ""
        return name.get_text().strip()

    def fetch_track_length(self, soup, container):
        time = container.find("length") or ""
        if not time:
            return ""
        time = int(time.get_text()) / 1000  # msecs -> secs
        times = []
        while time:
            times.append(time % 60)
            time /= 60
        times = list(str(ms) for ms in reversed(times))
        times[1:] = [ms.zfill(2) for ms in times[1:]]

        return ":".join(times)
