# -*- coding: utf-8 -*-


from . import Service, HTMLMixin


class Discogs(HTMLMixin, Service):

    def fetch_tracks(self, soup):
        return soup.select("#playlist- tr")

    def fetch_name(self, soup, container):
        name = container.find("span", class_="track_title")
        if not name:
            return ""
        return name.get_text().strip()

    def fetch_track_length(self, soup, container):
        time = container.find("td", class_="track_duration").span
        if not time:
            return ""
        return self.normalize_track_length(time.get_text().strip())
