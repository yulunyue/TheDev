from typing import List, Dict
from common.algo.base.node import Node, load_from_edges
from common.util.export import logger, defaultdict


class BeiZhenTree(Node):
    def __init__(self, key):
        super().__init__(key)
        self.bei_zen_list: List[BeiZhenTree] = []
        self.path_value = 0
        self.depth = 0

    def set_root(self):
        self.nodes: Dict[int, BeiZhenTree] = dict()
        self.depth = 0

        def dfs(t: BeiZhenTree, p: BeiZhenTree = None):
            self.nodes[t.key] = t
            if p is not None:
                t.bei_zen_list.append(p)
            for e in t.out_edges.values():
                dst: BeiZhenTree = e.dst
                if p and p.key == dst.key:
                    continue
                dst.depth = e.src.depth + 1
                dst.path_value = t.path_value + e.value
                dfs(dst, t)

        dfs(self, None)
        return self

    def bei_zhen(self):
        self.set_root()
        parent_idx = 0
        nodes: List[BeiZhenTree] = self.nodes.values()
        while nodes:
            q = nodes
            nodes = []
            for n in q:
                if parent_idx >= len(n.bei_zen_list):
                    continue
                pn = n.bei_zen_list[parent_idx]
                if parent_idx >= len(pn.bei_zen_list):
                    continue
                pnn = pn.bei_zen_list[parent_idx]
                n.bei_zen_list.append(pnn)
                nodes.append(n)
            parent_idx += 1
        return self

    def get_k_parent(self, f: "BeiZhenTree", k):
        i = 0
        while k > 0 and i < len(f.bei_zen_list):
            if k & 1:
                f = f.bei_zen_list[i]
            k = k >> 1
            i += 1
        return f

    def get_up_dis(self, dst: int) -> "BeiZhenTree":
        x: BeiZhenTree = self
        m = len(x.bei_zen_list)
        for i in range(m - 1, -1, -1):
            if i >= len(x.bei_zen_list):
                continue
            p = x.bei_zen_list[i]
            if self.path_value - p.path_value <= dst:  # 可以跳至多 d
                x = p
        return x

    def get_last_lcm_parent(self, f: "BeiZhenTree", t: "BeiZhenTree"):
        if f.depth < t.depth:
            t = self.get_k_parent(t, t.depth - f.depth)
        elif f.depth > t.depth:
            f = self.get_k_parent(f, f.depth - t.depth)
        if f.key == t.key:
            return f
        ret = f
        l = len(f.bei_zen_list) - 1
        for i in range(l, -1, -1):
            if i >= len(f.bei_zen_list) or i >= len(t.bei_zen_list):
                continue
            pf, pt = f.bei_zen_list[i], t.bei_zen_list[i]
            if pf.key != pt.key:
                f, t = pf, pt
            else:
                ret = pf
        return ret

    @classmethod
    def load_from_edges(cls, edges) -> Dict[any, "BeiZhenTree"]:
        return load_from_edges(cls, edges)
