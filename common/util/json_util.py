import json
from collections.abc import ValuesView
from common.exception import NotFoundError, ValidationError


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

    return json.dumps(
        oj,
        indent=indent,
        default=util,
        ensure_ascii=False,
    )


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
        fun(*args, **kw)
    except Exception as e:
        s = str(e)
    assert msg in s, s


def json_get(data, keys: str, default_value=None):
    if isinstance(keys, str):
        ks = keys.split(".")
    else:
        ks = keys
    r = data
    for key in ks:
        if key not in r:
            if default_value is None:
                raise NotFoundError("Key not found in data", context={"data": data, "keys": keys})
            return default_value
        r = r[key]
    return r


def json_has(data, keys: str):
    if isinstance(keys, str):
        ks = keys.split(".")
    else:
        ks = keys
    r = data
    for key in ks:
        if key not in r:
            return False
        r = r[key]
    return True


def json_set(data, keys: str, value):
    if isinstance(keys, str):
        ks = keys.split(".")
    else:
        ks = keys
    r = data
    for i, key in enumerate(ks):
        if key not in r:
            if i == len(ks) - 1:
                if callable(value):
                    value = value()
                r[key] = value
                return True
            r[key] = dict()
        elif i == len(ks) - 1:
            if r[key] != value and not callable(value):
                r[key] = value
                return True
        r = r[key]
    return False


def cmd_parse_json(s):
    ret = []
    i = 0
    value = ""
    json_lt = json_rt = 0
    while i < len(s):
        v = s[i]
        if v == " " and json_lt == 0:
            if value:
                ret.append(value)
            value = ""
        elif v == "{":
            json_lt += 1
            value += v
        elif v == "}":
            json_rt += 1
            value += v
        else:
            value += v
        if json_lt == json_rt and json_lt:
            try:
                ret.append(json.loads(value))
            except Exception as e:
                raise ValidationError("JSON parsing failed", context={"error": e, "value": value, "json": json_lt})
            value = ""
        i += 1
    return ret
