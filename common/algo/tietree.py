from typing import List


class TieNode:
    def __init__(self, size, key="", length=0, default_value=None, parent=None) -> None:
        self.size = size
        self.key = key
        self.childs: List[TieNode] = [None]*size
        self.fail: TieNode = None
        self.last: TieNode = None
        self.parent: TieNode = parent
        self.length = length
        self.default_value = default_value
        self.value = default_value

    def add(self, s):
        tmp = self
        for i in s:
            if tmp.childs[i] is None:
                tmp.childs[i] = TieNode(
                    self.size, length=tmp.length+1,
                    key=chr(ord('a')+i),
                    default_value=self.default_value,
                    parent=self.parent
                )
            tmp = tmp.childs[i]
        return tmp

    def key_str(self):
        keys = []
        p = self
        while p:
            keys.insert(0, p.key)
            p = p.parent
        return "".join(keys)

    def to_str(self):
        return f'key:{self.key_str()},fail:{self.fail.key_str()},last:{self.last.key_str()},value:{self.value}'

    def build_fail(self):
        self.fail = self.last = self
        q: List[TieNode] = []
        for i in range(self.size):
            if self.childs[i] is None:
                self.childs[i] = self
            else:
                self.childs[i].fail = self.childs[i].last = self
                q.append(self.childs[i])
        while q:
            cur = q.pop(0)
            for k, son in enumerate(cur.childs):
                if son is None:
                    cur.childs[k] = cur.fail.childs[k]
                    continue
                son.fail = cur.fail.childs[k]
                son.last = son.fail if son.fail.length else son.fail.last
                q.append(son)
