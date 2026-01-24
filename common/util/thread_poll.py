from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import time
import sys

from .thread_exec import ThreadExec


class ThreadManage:
    def __init__(self, max_workers=100) -> None:
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def get_task(self, func, args):
        return [ThreadExec().load(func, arg) for arg in args]

    def run(self, func, args):
        self.tasks = self.get_task(func, args)
        futures = [d.add_to_executor(self.executor) for d in self.tasks]
        ret = []
        for future in as_completed(futures):
            ret.append(future.result())
        return ret
