from typing import List, Dict


def load_from_edges(cls: "Node", edges):

    nodes: Dict[str, Node] = dict()
    for f, t, *args in edges:
        if f not in nodes:
            nodes[f] = cls(f)
        if t not in nodes:
            nodes[t] = cls(t)
        e = Edge(nodes[f], nodes[t]).load(*args)
        nodes[f].out_edges[t] = nodes[t].in_edges[f] = e
    return nodes


class Node:

    def __init__(self, key):
        self.key = key
        self.depth = 0
        self.in_edges: Dict[str, Edge] = {}
        self.out_edges: Dict[str, Edge] = {}

    def __repr__(self):
        return f"(key:{self.key})"


class Edge:
    def __init__(self, src, dst):

        self.src: Node = src
        self.dst: Node = dst

    def load(self, dst_value=1, src_value=1):
        self.src_value = src_value
        self.dst_value = dst_value
        return self
