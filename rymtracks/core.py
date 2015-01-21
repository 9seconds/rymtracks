# -*- coding: utf-8 -*-
"""
Core logic of RYMTracks.
"""


import concurrent.futures

from .services import Service


##############################################################################


__all__ = "execute",


##############################################################################


def execute(locations):
    """
    Just some function to be executed by main function.
    """

    tasks = [Service.produce(loc) for loc in locations]
    return [task.get_result() for task in tasks]
    # with concurrent.futures.ThreadPoolExecutor(len(locations)) as pool:
    #     return list(pool.map(lambda task: task.get_result(), tasks))
