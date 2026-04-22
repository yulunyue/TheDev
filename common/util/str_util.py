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
        from common.algo.base.nodes.node import Node

        return Node.load_from_edges(g)[head].show(f)

    def format_grid(self, n, m, f):
        ret = [[""] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                ret[i][j] = str(f[i, j])
        return "\n".join(["-" * m * 2] + [" ".join(row) for row in ret] + ["-" * m * 2])

    def get_mid_str(self, s: str, pre, end):
        pre_idx = s.find(pre)
        if pre_idx == -1:
            raise Exception(s, f"not find {pre}")
        s = s[pre_idx + len(pre) :]
        end_idx = s.find(end)
        if end_idx == -1:
            raise Exception(s, f"not find {end}")
        return s[:end_idx]
