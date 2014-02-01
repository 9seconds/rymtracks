# -*- coding: utf-8 -*-
"""
Core logic of RYMTracks. Actually there are some functions which uses
Tornado IO loop and invokes parsers.
"""


from .services import Service

from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return


##############################################################################


__all__ = "process_urls", "execute"


##############################################################################


try:
    import pycurl
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
except ImportError:
    pass


##############################################################################


@coroutine
def process_urls(urls, worker_pool):
    """
    Processes a list of urls with given worker pool.
    """
    tasks = [Service.produce(url, worker_pool) for url in urls]
    tasks = [task.get_task() for task in tasks if task is not None]
    finished_tasks = yield tasks
    raise Return(finished_tasks)


##############################################################################


def execute(urls):
    """
    Just some function to be executed by main function.
    """
    worker_pool = ThreadPoolExecutor(cpu_count() * 2 + 1)
    return IOLoop.instance().run_sync(lambda: process_urls(urls, worker_pool))
