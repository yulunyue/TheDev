from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import time


class ThreadExec:
    def load(self, func, args=None):
        self.func = func
        self.args = args
        return self

    def add_to_executor(self, executor: ThreadPoolExecutor):
        self.future = executor.submit(self.func, self.args)
        return self.future


class ThreadManage:
    def __init__(self) -> None:
        self.executor = ThreadPoolExecutor()

    def get_task(self, func, args):
        return [ThreadExec().load(func, arg) for arg in args]

    def run(self, func, args):
        self.tasks = self.get_task(func, args)
        futures = [d.add_to_executor(self.executor) for d in self.tasks]
        ret = []
        for future in as_completed(futures):
            ret.append(future.result())
        return ret
