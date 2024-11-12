import os
from typing import List
import json
from common.util.log import logger
from collections import defaultdict


def os_system(s: str):
    ret = os.system(s)
    if ret != 0:
        raise Exception(s)


def hash_any(c):
    res = ""
    if isinstance(c, dict):
        for k in sorted(c.keys()):
            res += k+hash_any(c[k])
    elif isinstance(c, list):
        for v in c:
            res += hash_any(v)
    else:
        res += str(c)
    return res


def dp(c: dict, k="", mp=None):
    if mp is None:
        mp = defaultdict(set)
    if isinstance(c, list):
        for i, v in enumerate(c):
            dp(v, i)
    elif isinstance(c, dict):
        for k, v in c.items():
            dp(v, k)
    else:
        mp[k].add(c)
    return mp


if __name__ == "__main__":
    print(hash_any(dict(a=3, b=[3, 4], c=dict(e=1))))
