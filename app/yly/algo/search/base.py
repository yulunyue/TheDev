
from common.algo.absearch import AlphaBateSearch, AbNode,State
from common.algo.mttsearch import MctsNode,MctsSearchTree
import sys
from app.yly.algo.manage import SolutionBase,View
import random

def shape1(AbNode:State):
    ret:State=AbNode(
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
        AbNode(
            AbNode(),
            AbNode()
        )
    )
    return ret.set_random_value()


class Solution(SolutionBase):
    _has_view=True
    def get_cases(self):
        shape1_json=shape1(State).dump()
        return [
            dict(root=shape1_json, search_type="mcts", result=""),
            dict(root=State(
                State(
                    State().set_value(-2),
                    State().set_value(-4),
                ),
                State().set_value(-3)
            ).dump(), result=""),
            dict(root=State(
                State().set_value(-2),
                State().set_value(-3)
            ).dump(), result="")
        ]

    def get_watch(self):
        return [
            View("root").graph()
        ]

    def init(self, root, search_type="", **kw):
        self.kw=kw
        self.search_type = search_type
        if search_type == 'mcts':
            self.root = MctsNode.load_from_json(**root)
            self.search_tree = MctsSearchTree()
        else:
            self.root = AbNode.load_from_json(**root)
            self.search_tree = AlphaBateSearch()


    def execute(self):
        return self.search_tree.search(self.root,**self.kw)


if __name__ == '__main__':
    Solution().run()
