from typing import List, Dict
from common.algo.base.edge import Edge


def load_from_edges(cls, edges):

    nodes = dict()
    for f, t, *args in edges:
        if f not in nodes:
            nodes[f] = cls(f)
        if t not in nodes:
            nodes[t] = cls(t)
        if len(args) == 0:
            Edge(nodes[f], nodes[t]).load(1)
            Edge(nodes[t], nodes[f]).load(1)
        elif len(args) == 1:
            Edge(nodes[f], nodes[t]).load(args[0])
            Edge(nodes[t], nodes[f]).load(args[0])
        elif len(args) == 2:
            Edge(nodes[f], nodes[t]).load(args[0])
            Edge(nodes[t], nodes[f]).load(args[1])
    return nodes


class Node:
    depth = 0
    value = 0

    def __init__(self, key):
        self.key = key
        self.edges: List[Edge] = []
