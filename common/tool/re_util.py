import re
from common.util.export import log


def wrap_ret(fun):
    def wrap(*args, **kw):
        a = fun(*args, **kw)
        if a is None:
            return a
        return a.group()

    return wrap


class ReUtil:
    def __init__(self, p):
        self.s = re.compile(p, re.MULTILINE | re.DOTALL)

    @wrap_ret
    def search(self, s):
        return self.s.search(s)

    def findall(self, s):
        return self.s.findall(s)

    @wrap_ret
    def match(self, s):
        return self.s.match(s)
