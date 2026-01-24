from typing import List
import re
from .re_util import ReUtil


class StrUtil:
    MATCH_FLAGS = None

    def __init__(self):
        self.ignore_matchs = []
        self.any_matchs = []

    def set_ignores(self, ignore_matchs: List[str]):
        self.ignore_matchs = [ReUtil(e) for e in ignore_matchs or []]
        return self

    def set_matchs(self, any_matchs: List[str]):
        self.any_matchs = [ReUtil(e) for e in any_matchs or []]
        return self

    def match(self, t: str):
        for s in self.ignore_matchs:
            if s.findall(t):
                return False
        if self.any_matchs:
            for s in self.any_matchs:
                if s.findall(t):
                    return True
            return False
        return True

    def format_pre0_bin(self, s, n):
        return format(s, f"0{n}b")

    def format(self, s: str, **kw):
        array = s.split("%{")
        result = array.pop(0)
        for v in array:
            idx = v.index("}")
            result += kw[v[:idx]] + v[idx + 1 :]
        return result

    def format_g_tree(self, g: List[List[int]], f, head=0):
        ret = ["---"]

        def dfs(u, p=-1, depth=0):
            ret.append(f'{" "*depth}-{u}: {f(u)}')
            if u >= len(g):
                return
            for k in g[u]:
                if k == p:
                    continue
                dfs(k, u, depth + 2)

        dfs(head)
        ret.append("---")
        return "\n".join(ret)
