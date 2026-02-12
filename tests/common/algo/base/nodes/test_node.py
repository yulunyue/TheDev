from common.algo.base.nodes.node import Node,
from common.algo.base.nodes.util import load_from_edges
from common.util.export import TestBase


class TestNode(TestBase):
    def test_base(self):
        nodes = load_from_edges(Node, [[0, 1], [0, 2]])
        root = nodes[0]
        self.expect(
            root.to_json(),
            {
                "nodes": {0: 0, 1: 0, 2: 0},
                "edges": [[0, 1, 0], [1, 0, 0], [0, 2, 0], [2, 0, 0]],
            },
        )
