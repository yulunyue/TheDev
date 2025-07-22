import json
import sys
import functools
import heapq
from typing import List, Dict
import math
from collections import defaultdict
import os
import random

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


class MockCf:
    dev = False

    def __init__(self):
        self.inputs = []

    def set_inputs(self, inputs: str):
        self.inputs = inputs.split("\n")
        return self

    def input(self):
        if os.path.exists("input.txt") and self.inputs is None:
            self.inputs = open("input.txt").read().split("\n")
        if self.dev:
            return self.inputs.pop(0)
        self.inputs.append(input())
        return self.inputs[-1]

    def ii(self):
        return [int(v) for v in self.input().split(" ")]

    def main(self):

        ans = self.run()
        if ans is None:
            return
        if isinstance(ans, list):
            self.output(len(ans))
            for d in ans:
                self.output(d)
        else:
            self.output(ans)

    _o = None

    def output(self, s):
        if self._o is None:
            self._o = open("output.txt", "w")
        self._o.write(f"{s}\n")


class MockCg(MockCf):
    def __init__(self):
        super().__init__()
        self.msgs = []

    def log(self, **kw):
        info = dict(inputs=self.inputs)
        info.update(kw)
        print(json.dumps(info), file=sys.stderr)
        self.inputs.clear()

    def output(self, s):
        print(s)


C = Constant()
