# -*- coding: utf-8 -*-


from . import Service, HTMLMixin


class BandCamp(Service, HTMLMixin):

    def fetch_tracks(self, soup):
        return soup.select("#track_table div.title")

    def fetch_name(self, soup, container):
        name = container.find("span", itemprop="name")
        if not name:
            return ""
        return name.get_text().strip()

    def fetch_time(self, soup, container):
        time = container.find("span", class_="time")
        if not time:
            return ""
        return self.normalize_track_length(time.get_text().strip())
