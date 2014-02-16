# -*- coding: utf-8 -*-
"""
Collection of formatters for RYMTracks.
"""


from six import print_, text_type
from utils import colored, msg


##############################################################################


# Width of terminal. Used by stdout formatter
STDOUT_WIDTH = 80

LOCATION_DELIMETER = msg("=", "green")
CSV_DELIMIETER = msg("|", "magenta")

EXCEPTION_COLOR = "red"
TITLE_COLOR = "green"


##############################################################################


def console(results):
    """
    Just prints results into your neat terminal window.
    """
    results = sorted(
        results,
        key=lambda res: (res.exception is None, res.location)
    )

    for idx, result in enumerate(results):
        if result.exception:
            title = msg(result.location, TITLE_COLOR, attrs=["bold"])
            title += msg(
                u" ({}) ".format(text_type(result.exception)),
                EXCEPTION_COLOR, attrs=["bold"]
            )
            title += LOCATION_DELIMETER * (STDOUT_WIDTH - len(title))
            print_(title)
            continue

        if len(results) > 1:
            title = msg(result.location + u" ", TITLE_COLOR)
            title += LOCATION_DELIMETER * (STDOUT_WIDTH - len(title))
            print_(title)

        for track_idx, (title, length) in enumerate(result.data, start=1):
            message = str(track_idx)
            message += CSV_DELIMIETER
            message += msg(title.replace("|", r"\|"), attrs=["bold"])
            message += CSV_DELIMIETER
            message += length
            print_(message)

        if idx < len(results) - 1:
            print_("")
