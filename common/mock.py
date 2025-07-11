import json
import sys
import functools
import heapq
from typing import List, Dict
import math

try:
    from sortedcontainers import SortedDict, SortedList, SortedSet
except Exception as e:
    pass
from collections import defaultdict


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log


class Constant:
    MOD = (10**9) + 7
    inf = float("inf")


class CgMock:
    msgs = []
    inputs = None

    def input(self):
        if self.inputs is None:
            r = input()
        else:
            r = self.inputs.pop(0)
        self.msgs.append(r)
        return r

    def ii(self):
        return [int(v) for v in self.input().split(" ")]

    def replay(self):
        pass

    def debug(self, **kw):
        debug_map = dict(inputs=self.msgs)
        debug_map.update(kw)
        print(json.dumps(debug_map), file=sys.stderr, flush=True)
        self.msgs.clear()

    def run(self):
        pass

    def main(self):
        print(self.run())

    def get_cases(self):
        return {}

    def set_inputs(self, inputs: str):
        self.inputs = inputs.split("\n")
        return self


C = Constant()
