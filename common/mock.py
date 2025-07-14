import json
import sys
import functools
import heapq
from typing import List, Dict
import math
from collections import defaultdict
import os

try:
    from sortedcontainers import SortedDict, SortedList, SortedSet
except Exception as e:
    pass


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
    def __init__(self):
        self.msgs = []
        self.inputs = None
        self.result = []
        self.dev = False

    def replay(self):
        pass

    def run(self):
        raise Exception("run_todo")

    def main(self):
        self.result.clear()
        ans = self.run()
        if ans is None:
            return
        if isinstance(ans, list):
            self.output(len(ans))
            for d in ans:
                self.output(d)
        else:
            self.output(ans)

    def get_cases(self):
        raise Exception("todo")

    def set_inputs(self, inputs: str):
        self.inputs = inputs.split("\n")
        return self


class MockCf(MockBase):
    def input(self):
        if os.path.exists("input.txt") and self.inputs is None:
            self.inputs = open("input.txt").read().split("\n")
        if self.inputs:
            return self.inputs.pop(0)
        return input()

    def ii(self):
        return [int(v) for v in self.input().split(" ")]

    _o = None

    def output(self, s):
        if self._o is None:
            self._o = open("output.txt", "w")
        self._o.write(f"{s}\n")


C = Constant()
