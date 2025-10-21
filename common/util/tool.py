import os
from typing import List
import json
from collections import defaultdict
import sys
import re
import json

UK_MAP = dict()


def uid(s):
    if s not in UK_MAP:
        UK_MAP[s] = -1
    UK_MAP[s] += 1
    return f"{s}_{UK_MAP[s]}"


def ii(s: str):
    ans = []
    for v in s.replace("\n", " ").split(" "):
        if not v:
            continue
        try:
            ans.append(int(v))
        except Exception as e:
            break
    return ans


def os_system(s: str):
    ret = os.system(s)
    if ret != 0:
        raise Exception(s)


def hash_any(c):
    res = ""
    if isinstance(c, dict):
        for k in sorted(c.keys()):
            res += k + hash_any(c[k])
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


def str_mid(s: str, size, fill="-"):
    if len(s) >= size:
        return s[:size]
    c = size - len(s)
    l, y = c // 2, c % 2
    return fill * l + s + fill * (l + y)


def url_to_json(params):
    args, kw = [], dict()
    if isinstance(params, str):
        params = params.split("&")
    for param in params:
        idx = param.find("=")
        if idx == -1:
            args.append(param)
        else:
            kw[param[:idx]] = param[idx + 1 :]
    return args, kw


def re_search(pattern, s):
    return re.search(pattern=pattern, string=s)


def json_dumps(oj, indent=2):
    def util(v):
        if isinstance(v, set):
            return list(v)
        if isinstance(v, (str, int, list, dict)):
            return v
        return str(v)

    return json.dumps(oj, indent=indent, default=util)


def merge_dict(src, dst):
    record = []

    def util(f, t, keys):
        if isinstance(f, dict) and isinstance(t, dict):
            for k, v in t.items():
                if k not in f:
                    f[k] = v
                    record.append(dict(method="insert", dst=v, keys=keys))
                else:
                    f[k] = util(f[k], t[k], keys + [k])
            return f
        else:
            if f != t:
                record.append(dict(method="update", src=f, dst=t, keys=keys))
            return t

    util(src, dst, [])
    return src, record

