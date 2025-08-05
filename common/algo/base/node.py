from typing import List, Dict


def load_from_edges(cls: "Node", edges):

    nodes: Dict[str, Node] = dict()
    for f, t, *args in edges:
        if f not in nodes:
            nodes[f] = cls(f)
        if t not in nodes:
            nodes[t] = cls(t)
        if len(args) == 0:
            ft = tf = 1
        elif len(args) == 1:
            ft = tf = args[0]
        else:
            ft = tf = args
        if ft is not None:
            nodes[f].out_edges[t] = Edge(nodes[f], nodes[t]).load(ft)
        if tf is not None:
            nodes[t].out_edges[f] = Edge(nodes[t], nodes[f]).load(tf)
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

    def load(self, value):
        self.value = value
        return self
