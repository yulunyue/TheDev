from common.util.export import List, Dict, defaultdict, logger


class TieNode:

    def __init__(self):
        self.childs = dict()

    def add(self, s) -> "TieNode":
        tmp = self
        for i in range(len(s)):
            if tmp.childs.get(s[i], None) is None:
                tmp.childs[s[i]] = self.__class__().set_key(s[: i + 1]).set_parent(tmp)
            tmp = tmp.childs[s[i]]
        return tmp

    def search(self, s):
        root = self
        ret: List[TieNode] = []
        for v in s:
            if v not in root.childs:
                return ret
            root: TieNode = root.childs[v]
            if root.value is not None:
                ret.append(root)
        return ret

    def set_key(self, key):
        self.key = key
        return self

    p: "TieNode" = None

    def set_parent(self, p):
        self.p = p
        return self

    value = None

    def set_value(self, v):
        self.value = v
        return self

    key = "_ROOT"

    def show(self):
        ret = ["----"]

        def dfs(n: TieNode, depth=0):
            v = str(n.value) if n.value is not None else ""
            ret.append(f"{' '*depth}-{n.key}: {v}")
            for v in n.childs.values():
                dfs(v, depth + 2)

        dfs(self)
        return "\n".join(ret + ["----"])
