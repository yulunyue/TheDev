import os
import sys
import json
from collections import defaultdict

from .time_util import time_format, time_change, time_strptime
from .crypto_util import (
    is_base64_code, base64_decode, base64_encode, b64_code,
    hash_any_str, md5, uid, ii, str_mid,
)
from .json_util import (
    json_dumps, assert_dict, merge_dict, asset_exception,
    json_get, json_has, json_set, cmd_parse_json,
)
from common.exception import NotFoundError


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


THE_DEV_LOGGER_PREFIX = "THE_DEV_LOGGER_PREFIX"
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
