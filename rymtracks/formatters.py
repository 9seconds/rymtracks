# -*- coding: utf-8 -*-
"""
Collection of formatters for RYMTracks.
"""


from six import print_, text_type


##############################################################################


# Width of terminal. Used by stdout formatter
STDOUT_WIDTH = 80


##############################################################################


def console(results):
    """
    Just prints results into your neat terminal window.
    """
    results = sorted(results, key=lambda res: (res.exception is None, res.url))

    for idx, result in enumerate(results):
        if result.exception:
            title = result.url + u" ({}) ".format(text_type(result.exception))
            print_(title.ljust(STDOUT_WIDTH, "="))
            continue
        if len(results) > 1:
            title = result.url + u" "
            print_(title.ljust(STDOUT_WIDTH, "="))
        for track_idx, (title, length) in enumerate(result.data, start=1):
            track_idx = str(track_idx)
            title = title.replace("|", r"\|").title()
            print_(track_idx + "|" + title + "|" + length)
        if idx < len(results) - 1:
            print_("")
