# -*- coding: utf-8 -*-
"""
Collection of formatters for RYMTracks.
"""


from __future__ import absolute_import, unicode_literals, print_function


STDOUT_WIDTH = 80


def justify(text):
    """
    Justifies text for stdout.
    """

    return text.ljust(STDOUT_WIDTH, "=")


def console(results):
    """
    Just prints results into your neat terminal window.
    """

    results = sorted(
        results, key=lambda res: (res.exception is not None, res.location)
    )

    for idx, result in enumerate(results):
        if result.exception:
            title = "{0} ({1}) ".format(
                result.location, result.exception
            )
            print(justify(title))
            continue

        if len(results) > 1:
            title = result.location + " "
            print(justify(title))

        for track_idx, (title, length) in enumerate(result.data, start=1):
            message = "{track} | {title} | {length}".format(
                track=track_idx,
                title=title.replace("|", r"\|"),
                length=length
            )
            print(message)

        if idx < len(results) - 1:
            print("")
