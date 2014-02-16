# -*- coding: utf-8 -*-
"""
Core logic of RYMTracks.
"""


from .services import Service

from concurrent.futures import ThreadPoolExecutor


##############################################################################


__all__ = "execute",


##############################################################################


def execute_task(task):
    """
    Task executor for ProcessPoolExecutor.
    """
    return task.get_result()


def execute(locations):
    """
    Just some function to be executed by main function.
    """
    tasks = [Service.produce(loc) for loc in locations]
    return [task.get_result() for task in tasks]
    with ThreadPoolExecutor(len(locations)) as task_pool:
        return list(task_pool.map(execute_task, tasks))
