from typing import List, Dict
from common.algo.base.node import Node, load_from_edges
from common.util.export import logger, defaultdict


class BeiZhenTree(Node):
    def __init__(self, key):
        super().__init__(key)
        self.bei_zen_map: Dict[int, BeiZhenTree] = dict()
        self.path = []
        self.path_value = 0

    def set_root(self):
        self.nodes: Dict[int, BeiZhenTree] = dict()
        self.depth = 0

        def dfs(t: BeiZhenTree, p: BeiZhenTree = None):
            self.nodes[t.key] = t
            t.bei_zen_map[0] = p
            t.path = (p.path if p else []) + [t]
            for e in t.out_edges.values():
                dst: BeiZhenTree = e.dst
                if p and p.key == dst.key:
                    continue
                dst.depth = e.src.depth + 1
                dst.path_value = t.path_value + e.dst_value
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
                pn = n.bei_zen_map.get(parent_idx)
                if pn is None:
                    continue
                n.bei_zen_map[parent_idx + 1] = pn.bei_zen_map.get(parent_idx)
                if n.bei_zen_map[parent_idx + 1]:
                    nodes.append(n)
            parent_idx += 1
        return self

    def get_k_parent(self, f: "BeiZhenTree", k):
        i = 0
        while k > 0 and f:
            if k & 1:
                f = f.bei_zen_map.get(i)
            k = k >> 1
            i += 1
        return f

    def get_last_lcm_parent(self, f: "BeiZhenTree", t: "BeiZhenTree"):
        if f.depth < t.depth:
            t = self.get_k_parent(t, t.depth - f.depth)
        elif f.depth > t.depth:
            f = self.get_k_parent(f, f.depth - t.depth)
        if f.key == t.key:
            return f
        ret = f
        l = len(f.bei_zen_map.keys()) - 1
        for i in range(l, -1, -1):
            pf, pt = f.bei_zen_map.get(i), t.bei_zen_map.get(i)
            if pf is None or pt is None:
                continue
            if pf.key != pt.key:
                f, t = pf, pt
            else:
                ret = pf
        return ret

    def get_dis2node(self, f: "BeiZhenTree", t: "BeiZhenTree"):
        p = self.get_last_lcm_parent(f, t)
        return f.path_value + t.path_value - 2 * p.path_value

    def get_path2node(self, f: "BeiZhenTree", t: "BeiZhenTree"):
        p = self.get_last_lcm_parent(f, t)
        return f.path[p.depth + 1 :][::-1] + t.path[p.depth :]

    @classmethod
    def load_from_edges(cls, edges) -> Dict[any, "BeiZhenTree"]:
        return load_from_edges(cls, edges)
