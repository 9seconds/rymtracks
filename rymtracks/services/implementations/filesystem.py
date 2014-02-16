# -*- coding: utf-8 -*-
"""
This module contains implementation of service on local filesystem. It uses
Mutagen library to access metainformation from music files.
"""


from ..base import Service, ParserResponse
from ...capitalization import capitalize

from collections import namedtuple
from itertools import chain
from os import access, R_OK, walk
from os.path import isdir, abspath, join as path_join
from math import ceil
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from six import PY2

if PY2:
    from mutagen import File
else:
    from mutagenx import File


###############################################################################


# Just convenient structure to store metainformation on each file
FileMeta = namedtuple(
    "FileMeta", ["disc", "track_number", "title", "length", "filename"]
)


###############################################################################


class FileSystem(Service):
    """
    Implementation of service for local filesystem.
    """

    @classmethod
    def normalize_walk_paths(cls, paths, root=None):
        """
        Normalizes paths or list of paths regarding to the root. It is
        convenient to use with os.walk which returns relative path names and
        if you want to convert them to absolute ones this convenient wrapper
        here for you.
        """
        if isinstance(paths, (list, tuple)):
            return [cls.normalize_walk_paths(path, root) for path in paths]
        if root is not None:
            root = abspath(root)
            return path_join(root, paths)
        return abspath(paths)

    @staticmethod
    def get_metadata(meta, attr, default=None):
        """
        Just small shortcut to extract data from Mutagen instance.
        """
        return meta.get(attr, [default])[0]

    def get_result(self):
        if not (isdir(self.location) and access(self.location, R_OK)):
            return ParserResponse(self.location, [], Exception("Empty list"))

        visited = set()
        futures = []
        with ThreadPoolExecutor(cpu_count()) as mutagen_pool:
            for root, dirs, files in walk(self.location, followlinks=True):
                root = self.normalize_walk_paths(root)
                if root in visited:
                    continue
                visited.add(root)
                files = self.normalize_walk_paths(files, root)
                futures.append(mutagen_pool.map(self.fetch_meta, files))

            futures = chain.from_iterable(futures)
            results = [result for result in futures if result is not None]

        results.sort(
            key=lambda item: (item.disc, item.track_number, item.filename)
        )
        results = tuple(
            (capitalize(item.title), self.normalize_track_length(item.length))
            for item in results
        )

        return ParserResponse(self.location, results, None)

    def fetch_meta(self, filename):
        """
        Extracts metainformation from the given file and converts it to
        FetchMeta instance.
        """
        try:
            meta = File(filename, easy=True)
        except IOError:
            meta = None
        if meta is None:
            return None

        disc_number = self.get_metadata(meta, "discnumber", "1")
        track_number = self.get_metadata(meta, "tracknumber", "1")
        title = self.get_metadata(meta, "title", "")
        length = int(ceil(meta.info.length))
        length = self.second_to_timestamp(length)

        return FileMeta(disc_number, track_number, title, length, filename)