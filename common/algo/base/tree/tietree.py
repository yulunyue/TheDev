from common.util.export import List, Dict, defaultdict, logger


class TieNode:

    def __init__(self, key="R", p=None):
        self.size = 0
        self.depth = -1
        self.key = key
        self.p = p
        self.load()

    def load(self):
        self.childs: Dict[str, TieNode] = defaultdict(lambda: None)
        return self

    def get(self, key):
        if self.childs[key] is None:
            self.childs[key] = self.__class__(key, self).load()
        return self.childs[key]

    def load(self):
        return self

    def update_pos(self, idx):
        raise NotImplementedError

    def add(self, s, idx=None) -> "TieNode":
        tmp = self
        tmp.size += 1
        for i in range(len(s)):
            tmp = tmp.get(s[i])
            if idx is not None:
                tmp.update_pos(idx)
            tmp.size += 1

        return tmp

    def remove(self, s):
        tmp = self
        tmp.size -= 1
        for i in range(len(s)):
            tmp = tmp.childs[s[i]]
            tmp.size -= 1

    def search(self, s):
        root = self
        ret: List[TieNode] = [root]
        for v in s:
            if v not in root.childs:
                return ret
            root: TieNode = root.childs[v]
            if root.size == 0:
                return ret
            ret.append(root)
        return ret

    value = 0

    def set_value(self, v):
        self.value = v
        return self

    def to_str(self):
        return f"{self.value}:{self.size}"

    def show(self):
        ret = ["----"]

        def dfs(n: TieNode, depth=0):
            ret.append(f"{' '*depth}-{n.key}: {n.to_str()}")
            for v in n.childs.values():
                dfs(v, depth + 2)

        dfs(self)
        return "\n".join(ret + ["----"])

    def get_next_child(self):
        raise NotImplementedError

    def query(self, s):
        root = self
        for v in s:
            u = self.get_next_child(v)
            if u not in root.childs or root.childs[u] == 0:
                return root
            root: TieNode = root.childs[v]
        return root
