from typing import List, Dict
from common.algo.base.edge import Edge


def load_from_edges(cls: "Node", edges):

    nodes: Dict[str, Node] = dict()
    edges = []
    for f, t, *args in edges:
        if f not in nodes:
            nodes[f] = cls(f)
        if t not in nodes:
            nodes[t] = cls(t)
        e = Edge(nodes[f], nodes[t]).load(*args)
        nodes[f].out_edges[t] = nodes[t].out_edges[f] = e
        edges.append(e)
    return nodes, edges


class Node:

    def __init__(self, key):
        self.key = key
        self.in_edges: Dict[str, Edge] = {}
        self.out_edges: Dict[str, Node] = {}

    def __repr__(self):
        return f"(key:{self.key})"
