import re
from common.util.export import log


class ReUtil:
    def __init__(self, p):
        self.s = re.compile(p)

    def search(self, s):
        return self.s.search(s).group()

    def match(self, s):
        ret: re.Match = self.s.match(s)
        result = None
        if ret is not None:
            result = ret.group()
        log.map(p=self.s, s=s, result=result)
        return result
