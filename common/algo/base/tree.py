from typing import List, Dict
from common.algo.base.node import Node, load_from_edges


class TreeNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.parents: Dict[int, TreeNode] = dict()

    def set_root(self):
        self.nodes: Dict[int, TreeNode] = dict()
        self.depth = 0

        def dfs(t: TreeNode, p: TreeNode = None):
            self.nodes[t.key] = t

            t.parents[0] = p
            for e in t.edges:
                if p and p.key == e.dst.key:
                    continue
                e.dst.depth = e.src.depth + 1
                e.dst.value = e.value + e.src.value
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
                if v.parents.get(parent_idx) is None:
                    continue
                break_flag = False
                pk = v.parents[parent_idx].key
                v.parents[parent_idx + 1] = self.nodes[pk].parents.get(parent_idx)
            parent_idx += 1
        return self

    def get_k_parent(self, f: "TreeNode", k):
        i = 0
        while k > 0 and f:
            if k & 1:
                f = f.parents.get(i)
            k = k >> 2
            i += 1
        return f

    def get_last_lcm_parent(self, f: "TreeNode", t: "TreeNode"):
        return f

    def get_dis2node(self, f: "TreeNode", t: "TreeNode"):
        p = self.get_last_lcm_parent(f, t)
        return f.value + t.value - 2 * p.value

    @classmethod
    def load_from_edges(cls, edges) -> Dict[any, "TreeNode"]:
        return load_from_edges(cls, edges)
