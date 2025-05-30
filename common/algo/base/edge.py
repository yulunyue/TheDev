class Edge:
    def __init__(self, src, dst):
        from common.algo.base.node import Node

        self.src: Node = src
        self.dst: Node = dst
        self.src.edges.append(self)

    def load(self, value):
        self.value = value
        return self
