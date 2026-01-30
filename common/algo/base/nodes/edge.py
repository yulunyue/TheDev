from .node import Node


class Edge:
    value = None

    def __init__(self, src, dst):
        self.src: Node = src
        self.dst: Node = dst

    def load(self, value):
        self.value = value
        return self

    def get_value(self):
        return self.value
