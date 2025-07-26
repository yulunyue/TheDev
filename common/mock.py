import json
import sys
import functools
import heapq
from typing import List, Dict
import math
from collections import defaultdict
import os
import random
from common.tool.export import ThreadRecord

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


class MockCf(ThreadRecord):
    dev = False
    inputs = None

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

    _o = None

    def output(self, s):
        if self._o is None:
            self._o = open("output.txt", "w")
        self._o.write(f"{s}\n")


class MockCg(MockCf):
    name = ""

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

    @classmethod
    def main_py(cls):
        return f"app/yly/game/envs/{cls.name}/cg.py"

    @classmethod
    def tmp_dir(cls):
        return f"data/cg/{cls.name}"


C = Constant()
