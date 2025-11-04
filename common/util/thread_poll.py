from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import time
import sys


class ThreadExec:
    def load(self, func, args=None):
        self.func = func
        self.args = args
        return self

    def add_to_executor(self, executor: ThreadPoolExecutor):
        self.future = executor.submit(self.func, self.args)
        return self.future


def progress_bar(current, total, bar_length=100, msg=""):
    percent = float(current) * 100 / total
    arrow = "-" * int(percent / 100 * bar_length - 1) + ">"
    spaces = " " * (bar_length - len(arrow))
    sys.stdout.write(f"\r{msg}进度: [{arrow}{spaces}] [{current}/{total}]")
    sys.stdout.flush()
    if current == total:
        print("")


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
            progress_bar(len(ret), len(self.tasks))
        return ret
