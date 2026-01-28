from .node import Node


class Edge:
    def __init__(self, src, dst):
        self.src: Node = src
        self.dst: Node = dst

    def load(self, value):
        self.value = value
        return self
