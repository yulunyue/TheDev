import json
import sys
import functools
import heapq
from typing import List, Dict
import math
from collections import defaultdict

try:
    from sortedcontainers import SortedDict, SortedList, SortedSet
except Exception as e:
    pass


from common.tool.io import Io, IoTxtFile


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log


class Constant:
    MOD = (10**9) + 7
    inf = float("inf")


class MockBase:
    io = Io()

    def __init__(self):
        self.msgs = []
        self.inputs = None
        self.result = []
        self.dev = False

    def replay(self):
        pass

    def main(self):
        raise Exception("main_todo")

    def run(self):
        self.result.clear()
        ans = self.main()
        if ans is None:
            return
        if isinstance(ans, list):
            self.io.output(len(ans))
            for d in ans:
                self.io.output(d)
        else:
            self.io.output(ans)

    def get_cases(self):
        return {}

    def set_inputs(self, inputs: str):
        self.inputs = inputs.split("\n")
        return self


C = Constant()
