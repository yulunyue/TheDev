from typing import List, Dict
from common.algo.base.node import Node, load_from_edges
from common.util.export import logger


class TreeNode(Node):

    def set_root(self):
        self.nodes: Dict[int, TreeNode] = dict()
        self.depth = 0

        def dfs(t: TreeNode, p: TreeNode = None):
            self.nodes[t.key] = t
            t.bei_zen_map[0] = p
            t.path = (p.path if p else []) + [t]
            for e in t.edges:
                if p and p.key == e.dst.key:
                    continue
                e.dst.depth = e.src.depth + 1
                e.dst.path_value = e.src.path_value + e.value
                dfs(e.dst, e.src)

        dfs(self, None)
        return self

    def bei_zhen(self):
        self.set_root()
        parent_idx = 0
        break_flag = False
        while not break_flag:
            break_flag = True
            for k, v in self.nodes.items():
                if v.bei_zen_map.get(parent_idx) is None:
                    continue
                break_flag = False
                pk = v.bei_zen_map[parent_idx].key
                v.bei_zen_map[parent_idx + 1] = self.nodes[pk].bei_zen_map.get(
                    parent_idx
                )
            parent_idx += 1
        return self

    def get_k_parent(self, f: "TreeNode", k):
        i = 0
        while k > 0 and f:
            if k & 1:
                f = f.bei_zen_map.get(i)
            k = k >> 1
            i += 1
        return f

    def get_last_lcm_parent(self, f: "TreeNode", t: "TreeNode"):
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

    def get_dis2node(self, f: "TreeNode", t: "TreeNode"):
        p = self.get_last_lcm_parent(f, t)
        return f.path_value + t.path_value - 2 * p.path_value

    def get_path2node(self, f: "TreeNode", t: "TreeNode"):
        p = self.get_last_lcm_parent(f, t)
        return f.path[p.depth + 1 :][::-1] + t.path[p.depth :]

    @classmethod
    def load_from_edges(cls, edges) -> Dict[any, "TreeNode"]:
        return load_from_edges(cls, edges)
