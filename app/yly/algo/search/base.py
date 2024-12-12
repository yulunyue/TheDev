
from common.algo.absearch import AlphaBateSearch, AbNode
import sys
from app.yly.algo.manage import SolutionBase,View
import random
# random.seed(7)
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
        return [
            dict(root=shape1(AbNode).to_json(), result="")
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
