from typing import List, Dict


class Node:

    def __init__(self, key):
        from .edge import Edge

        self.key = key
        self.depth = 0
        self.in_edges: Dict[str, Edge] = {}
        self.out_edges: Dict[str, Edge] = {}

    def show(self):
        pass

    def get_value(self):
        return 0

    def to_json(self):
        nodes, edges = dict(), []

        def dfs(u: Node):
            if u.key in nodes:
                return
            nodes[u.key] = u.get_value()
            for k, e in u.out_edges.items():
                edges.append([e.src.key, e.dst.key, e.get_value()])
                dfs(e.dst)

        dfs(self)
        return dict(nodes=nodes, edges=edges)

    @classmethod
    def load_from_edges(cls, edges):
        from .util import load_from_edges

        return load_from_edges(cls, edges)

    def draw(self, path):
        from common.third_util.view.pygraphviz_util import PyGraphViz

        PyGraphViz().load(path).draw(**self.to_json())
