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
