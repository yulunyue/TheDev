from typing import List, Dict


class Node:

    def __init__(self, key):
        from .edge import Edge

        self.parent: Node = Node
        self.key = key
        self.depth = 0
        self.in_edges: Dict[str, Edge] = {}
        self.out_edges: Dict[str, Edge] = {}

    def set_parent(self, p: "Node"):
        self.parent = p
        return self

    def set_size(self, size):
        self.size = size
        return self

    def get_value(self):
        return 0

    def dfs(self, fn, p=None):
        fn(self, p)
        for e in self.out_edges.values():
            if p and e.dst.key == p.src.key:
                continue
            e.dst.dfs(fn, e)

    def to_json(self):
        nodes, edges = dict(), []
        from .edge import Edge

        def util(n: Node, e: Edge):
            nodes[n.key] = n.get_value()
            if e is not None:
                edges.append([e.src.key, e.dst.key, e.get_value()])

        self.dfs(util)
        return dict(nodes=nodes, edges=edges)

    @classmethod
    def load_from_edges(cls, edges):
        from .util import load_from_edges

        return load_from_edges(cls, edges)

    def draw(self, path):
        from common.third_util.view.pygraphviz_util import PyGraphViz

        PyGraphViz().load(path).draw(**self.to_json())

    def show(self, fn=None):
        ret = ["---"]
        from .edge import Edge

        def util(u, p=-1, depth=0):
            ret.append(f'{" "*depth}-{u}: {fn(u)}')

        self.dfs(util)
        ret.append("---")
        return "\n".join(ret)
