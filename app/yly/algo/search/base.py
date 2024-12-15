
from common.algo.absearch import AlphaBateSearch, AbNode
import sys
from app.yly.algo.manage import SolutionBase,View
import random

def shape1(AbNode):
    return AbNode(
        AbNode(
            AbNode(
                AbNode(),
                AbNode()
            ),
            AbNode(),
            AbNode(
                AbNode(),
                AbNode()
            ),
        ),
        AbNode(
            AbNode(),
            AbNode(
                AbNode(),
                AbNode()
            ),
            AbNode()
        ),
        AbNode(
            AbNode(
                AbNode(),
                AbNode(),
                AbNode()
            ),
            AbNode(),
            AbNode()
        ),
        AbNode()
    ).init()


class Solution(SolutionBase):
    _has_view=True
    def get_cases(self):
        random.seed(4)
        return [
            dict(root=shape1(AbNode).dump(), result=""),
            dict(root=AbNode(
                AbNode(
                    AbNode().set_value(-2),
                    AbNode().set_value(-4),
                ),
                AbNode().set_value(-3)
            ).dump(), result=""),
            dict(root=AbNode(
                AbNode().set_value(-2),
                AbNode().set_value(-3)
            ).dump(), result="")
        ]

    def get_watch(self):
        return [
            View("root").graph()
        ]

    def init(self, root, **kw):
        self.root = AbNode.load_from_json(**root)
        self.ab = AlphaBateSearch()


    def execute(self):
        return self.ab.search(last_move=self.root)


if __name__ == '__main__':
    Solution().run()
