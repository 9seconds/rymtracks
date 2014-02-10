# -*- coding: utf-8 -*-
"""
Core logic of RYMTracks.
"""


from .services import Service

from concurrent.futures import ProcessPoolExecutor


##############################################################################


__all__ = "execute",


##############################################################################


def execute_task(task):
    """
    Task executor for ProcessPoolExecutor.
    """
    return task.get_result()


def execute(urls):
    """
    Just some function to be executed by main function.
    """
    tasks = [Service.produce(url) for url in urls]
    with ProcessPoolExecutor(len(urls)) as task_pool:
        return list(task_pool.map(execute_task, tasks))
