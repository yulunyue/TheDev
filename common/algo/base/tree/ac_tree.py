from .tietree import TieNode


class AcTreeNode(TieNode):
    cur = None
    son = None

    def __init__(
        self, key, keys, depth=0, default_value=None, parent=None, root=None
    ) -> None:
        self.key = key
        self.keys = keys
        self.idx = TieNode.idx
        TieNode.idx += 1
        self.childs: Dict[str, TieNode] = {k: None for k in keys}
        self.fail: TieNode = None
        # self.last: TieNode = None
        self.root: TieNode = None
        self.parent: TieNode = parent
        self.depth = depth
        self.default_value = default_value
        self.value = default_value

    def build_fail(self):
        self.fail = self
        q: List[TieNode] = []
        for k in self.childs:
            if self.childs[k] is None:
                self.childs[k] = self
            else:
                self.childs[k].fail = self
                q.append(self.childs[k])
        while q:
            TieNode.cur = q.pop(0)
            for k, son in TieNode.cur.childs.items():
                if son is None:
                    TieNode.cur.childs[k] = TieNode.cur.fail.childs[k]
                    continue
                TieNode.son = son
                TieNode.son.fail = TieNode.cur.fail.childs[k]
                # son.last = son.fail if son.fail.depth else son.fail.last
                q.append(TieNode.son)
