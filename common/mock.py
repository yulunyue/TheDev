import json
import sys
import functools
import heapq
from typing import List, Dict
import math


def get_log(*args, **kw):
    pass


class logger:
    info = get_log
    map = get_log
    debug = get_log


class Constant:
    MOD = (10**9) + 7
    inf = float("inf")


C = Constant()
