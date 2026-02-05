import os
from typing import List
import json
from collections import defaultdict
import sys
import re
import json
import hashlib
import base64

UK_MAP = dict()


def uid(s):
    if s not in UK_MAP:
        UK_MAP[s] = -1
    UK_MAP[s] += 1
    return f"{s}_{UK_MAP[s]}"


def base64_encode(s: str):
    return base64.b64encode(s.encode()).decode()


def ii(s: str):
    ans = []
    for v in s.replace("\n", " ").split(" "):
        if not v:
            continue
        try:
            ans.append(int(v))
        except Exception as e:
            pass
    return ans


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


def md5(c: str):
    h = hashlib.md5(c.encode())
    return h.hexdigest()


def str_mid(s: str, size, fill="-"):
    if len(s) >= size:
        return s[:size]
    c = size - len(s)
    l, y = c // 2, c % 2
    return fill * l + s + fill * (l + y)


def cmd_parse(s: str):
    args, kw = [], dict()
    if isinstance(s, str):
        s = s.split(" ")
    for v in s:
        key, *value = v.split("=")
        if value:
            kw[key] = "=".join(value)
        else:
            args.append(key)
    return args, kw


THE_DEV_LOGER_PREFIX = "THE_DEV_LOGER_PREFIX"
SYS_ARGS, SYS_KW = cmd_parse(sys.argv[1:])


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


def dict_to_str(indent=" ", **kw):
    if isinstance(indent, int):
        return json_dumps(kw, indent=indent)
    ret = []
    for k in kw.keys():
        v = kw[k]
        if isinstance(v, float):
            v = "%.3f" % v
        ret.append(f"{k}={v}")
    return indent.join(ret)


def json_dumps(oj, indent=None):
    from ..tool.base_class.model import BaseModel

    def util(v):
        if isinstance(v, set):
            return list(v)
        if isinstance(v, (str, int, list, dict)):
            return v
        if hasattr(v, "to_json"):
            return v.to_json()
        if isinstance(v, BaseModel):
            return v.get_value()
        return str(v)

    return json.dumps(oj, indent=indent, default=util, ensure_ascii=False)


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
