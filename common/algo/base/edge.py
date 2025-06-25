class Edge:
    def __init__(self, src, dst):
        from common.algo.base.node import Node

        self.src: Node = src
        self.dst: Node = dst

    def load(self, src_value=1, dst_value=1):
        self.src_value = src_value
        self.dst_value = dst_value
        return self
