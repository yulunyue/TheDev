import json
import sys
import functools
import heapq
from typing import List, Dict
import math
from sortedcontainers import SortedDict, SortedList, SortedSet


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
    def input(self):
        r = input()
        return r

    def replay(self):
        pass

    def debug(self, action):
        print(f"Debug messages...:{action}", file=sys.stderr, flush=True)


C = Constant()
