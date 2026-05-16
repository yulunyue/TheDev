import hashlib
import base64


def is_base64_code(s: str):
    try:
        s = base64.b64decode(s, validate=True)
        return True
    except Exception as e:
        return False


def base64_decode(s: str):
    s = base64.b64decode(s)
    return s


def base64_encode(s: str):
    if isinstance(s, str):
        s = s.encode()
    return base64.b64encode(s).decode()


def b64_code(s: str):
    try:
        s = base64.b64decode(s, validate=True).decode()
        return s
    except:
        return base64.b64encode(s.encode()).decode()


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
            pass
    return ans


def str_mid(s: str, size, fill="-"):
    if len(s) >= size:
        return s[:size]
    c = size - len(s)
    l, y = c // 2, c % 2
    return fill * l + s + fill * (l + y)
