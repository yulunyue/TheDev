from common.util.export import List, Dict
from .node import Node
from .edge import Edge


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
