# -*- coding: utf-8 -*-


from . import Service, HTMLMixin


class ITunes(Service, HTMLMixin):

    def fetch_tracks(self, soup):
        tracks = soup.select(
            "div.track-list .tracklist-content-box > .tracklist-table"
        )
        if tracks:
            return tracks[0].select("tr.song")
        return []

    def fetch_name(self, soup, container):
        name = container.find("td", class_="name")
        if not name:
            return ""
        name = name.find("span", class_="text")
        return name.get_text().strip() if name else ""

    def fetch_time(self, soup, container):
        time = container.find("td", class_="time")
        if not time:
            return ""
        time = time.find("span", class_="text")
        return self.normalize_track_length(time.get_text().strip()) if time else ""
