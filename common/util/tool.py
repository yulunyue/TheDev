import os
from typing import List
import json
from collections import defaultdict
import sys
import re
import json
import hashlib
import base64
import time
from collections.abc import ValuesView


def time_format(timestamp):
    time_struct = time.localtime(timestamp)
    format_date = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
    return format_date


UK_MAP = dict()


def uid(s):
    if s not in UK_MAP:
        UK_MAP[s] = -1
    UK_MAP[s] += 1
    return f"{s}_{UK_MAP[s]}"


def is_base64_code(s: str):
    try:
        s = base64.b64decode(s, validate=True)
        return True
    except Exception as e:
        return False


def base64_decode(s: str):
    s = base64.b64decode(s).decode()
    return s


def base64_encode(s: str):
    return base64.b64encode(s.encode()).decode()


def b64_code(s: str):
    try:
        s = base64.b64decode(s, validate=True).decode()
        return s
    except:
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


def hash_any_str(c):
    res = ""
    if isinstance(c, dict):
        for k in sorted(c.keys()):
            res += k + hash_any_str(c[k])
    elif isinstance(c, list):
        for v in c:
            res += hash_any_str(v)
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


def url_parse(s: str):
    idx = s.find("?")
    if idx == -1:
        return s, [], dict()
    else:
        args, kw = url_to_json(s[idx + 1 :])
        return s[:idx], args, kw


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
    from ..tool.base_class.base_model.model import BaseModel

    def util(v):
        if isinstance(v, set):
            return list(v)
        if isinstance(v, (str, int, list, dict)):
            return v
        if hasattr(v, "to_json"):
            return v.to_json()
        if isinstance(v, BaseModel):
            return v.get_value()
        if isinstance(v, ValuesView):
            return list(v)
        return str(v)

    return json.dumps(oj, indent=indent, default=util, ensure_ascii=False)


def assert_dict(a, b):
    a, b = json_dumps(a), json_dumps(b)
    assert a == b


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


def asset_exception(fun, *args, msg="", **kw):
    s = ""
    try:
        fun(*args, **ke)
    except Exception as e:
        s = str(e)
    assert s, msg
