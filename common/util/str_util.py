from typing import List
import re


class StrUtil:
    MATCH_FLAGS = None

    def __init__(self):
        self.prefixs = []

    def set_ignores(self, ignore_matchs: List[str]):
        self.ignore_matchs = [re.compile(e) for e in ignore_matchs]

    def set_matchs(self, any_matchs: List[str]):
        self.any_matchs = [re.compile(e) for e in any_matchs]
        return self

    def match(self):
        if self.ignore_matchs:
            return True
        return False

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
