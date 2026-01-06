from typing import List


class StrUtil:
    def __init__(self):
        self.prefixs = []

    def str_prefix_match(self, s: str):
        for p in self.prefixs:
            if s.startswith(p):
                return True
        return False

    def format_pre0_bin(self, s, n):
        return format(s, f"0{n}b")

    def set_prefix(self, prefixs: List[str]):
        self.prefixs = prefixs
        return self

    def match(self):
        if self.str_prefix_match():
            return True
        return False

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
