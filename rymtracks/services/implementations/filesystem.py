# -*- coding: utf-8 -*-
"""
This module contains implementation of service on local filesystem. It uses
Mutagen library to access metainformation from music files.
"""


from __future__ import absolute_import, unicode_literals

import collections
import itertools
import operator
import os
import os.path
import math
import multiprocessing

import concurrent.futures
import six

if six.PY2:
    import mutagen
else:
    import mutagenx as mutagen

from ..service import Service, ParserResponse
from ...capitalization import capitalize


# Just convenient structure to store metainformation on each file
FileMeta = collections.namedtuple(
    "FileMeta", ["disc", "track_number", "title", "length", "filename"]
)


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
            root = os.path.abspath(root)
            return os.path.join(root, paths)
        return os.path.abspath(paths)

    @staticmethod
    def get_metadata(meta, attr, default=None):
        """
        Just small shortcut to extract data from Mutagen instance.
        """

        return meta.get(attr, [default])[0]

    def get_result(self):
        if not (os.path.isdir(self.location) and os.access(self.location, os.R_OK)):
            return ParserResponse(self.location, [], Exception("Empty list"))

        visited = set()
        futures = []
        with concurrent.futures.ThreadPoolExecutor(multiprocessing.cpu_count()) as mutagen_pool:
            for root, dirs, files in os.walk(self.location, followlinks=True):
                root = self.normalize_walk_paths(root)
                if root in visited:
                    continue
                visited.add(root)

                files = self.normalize_walk_paths(files, root)
                futures.append(mutagen_pool.map(self.fetch_meta, files))

            futures = itertools.chain.from_iterable(futures)
            results = [result for result in futures if result is not None]

        results.sort(key=operator.attrgetter("disc", "track_number", "filename"))
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
            meta = mutagen.File(filename, easy=True)
        except IOError:
            meta = None
        if meta is None:
            return None

        disc_number = self.get_metadata(meta, "discnumber", "1")
        track_number = self.get_metadata(meta, "tracknumber", "1")
        title = self.get_metadata(meta, "title", "")
        length = int(math.ceil(meta.info.length))
        length = self.second_to_timestamp(length)

        return FileMeta(disc_number, track_number, title, length, filename)