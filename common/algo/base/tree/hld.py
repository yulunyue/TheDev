from ..nodes.node import Node
from ..nodes.edge import Edge
from common.util.export import List
from .segtree import SegTreeNode


class HeavyNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.heavy: HeavyNode = None
        self.dfn = 0
        self.top: HeavyNode = None


class HLD:
    def set_seg(self, seg):
        self.seg: SegTreeNode = seg
        return self

    def set_root(self, root: HeavyNode):
        self.root = root
        self.dfs1(root, None)
        self.timer = 0
        self.rnk: List[HeavyNode] = []
        self.dfs2(root, root)
        return self

    def dfs1(self, u: HeavyNode, p: Edge):
        u.set_parent(None if p is None else p.src)
        u.size = 1
        max_sz = 0
        for e in u.out_edges.values():
            if p and e.dst.key == p.src.key:
                continue
            v = e.dst
            v.depth = u.depth + 1
            self.dfs1(v, e)
            u.size += v.size
            if u.size > max_sz:
                max_sz = u.size
                u.heavy = v

    def dfs2(self, u: HeavyNode, tp: HeavyNode):
        u.dfn = self.timer
        self.timer += 1
        u.top = tp
        self.rnk.append(u)

        if u.heavy:
            self.dfs2(u.heavy, tp)
        for e in u.out_edges.values():
            v = e.dst
            if u.parent == v or v == u.heavy:
                continue
            self.dfs2(v, v)

    def update_path(self, u: HeavyNode, v: HeavyNode, val):
        while u.top != v.top:
            if u.top.depth < v.top.depth:
                u, v = v, u
            self.seg.update(u.top.dfn, u.dfn, val)
            u = u.top.parent
        if u.depth > v.depth:
            u, v = v, u
        self.seg.update(u.dfn, v.dfn, val)

    def query_path(self, u: HeavyNode, v: HeavyNode, res=0):
        while u.top != v.top:
            if u.top.depth < v.top.depth:
                u, v = v, u
            value = self.seg.query(u.top.dfn, u.dfn)
            res = self.seg.merge(value, res)
            u = u.top.parent
        if u.depth > v.depth:
            u, v = v, u
        value = self.seg.query(u.dfn, v.dfn)
        res = self.seg.merge(value, res)
        return res

    def update_subtree(self, u: HeavyNode, val):
        self.seg.update(u.dfn, u.dfn + u.size - 1, val)

    def query_subtree(self, u: HeavyNode):
        return self.seg.query(u.dfn, u.dfn + u.size - 1)
