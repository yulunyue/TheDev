import re


class ReUtil:
    def __init__(self, p):
        self.s = re.compile(p)

    def search(self, s):
        return self.s.search(s).group()

    def match(self, s):
        ret: re.Match = self.s.match(s)
        if ret is not None:
            return ret.group()
        return None
