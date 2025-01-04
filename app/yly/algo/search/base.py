
from common.algo.absearch import AlphaBateSearch, AbNode,State
from common.algo.mttsearch import MctsNode,MctsSearchTree
import sys
from app.yly.algo.manage import SolutionBase,View
import random
from typing import List
class StateView(State):
    NODE_ID=0
    def __init__(self,*args):
        self.key = StateView.NODE_ID
        StateView.NODE_ID+=1
        self.root:State = None
        self.cur:State = None
        self.parent:State = None
        self.childs: List[State] = list(args)
        super().__init__()

    def load(self,fun=None):
        def dfs(c:State,depth):
            c.root = self
            c.depth = depth
            if len(c.childs)==0:
                if fun:
                    c.state_value=c.value=fun()        
                return c.state_value
            c.state_value=0
            for v in c.childs:
                c.state_value+=dfs(v,depth+1)
            return c.state_value
        dfs(self,0)       
        return self
    def get_nexts(self):
        return self.childs
    def __id__(self) -> int:
        return f'{self.value}'
    
    def __str__(self) -> str:
        cur_key=str(self.root.cur.key if self.root and self.root.cur else '')
        return cur_key+self.__id__()+"".join([v.__id__() for v in self.childs])


def shape1(AbNode:StateView):
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
    random.seed(7)
    return ret.load(lambda *args:random.randint(-10,10))



class AbSearchState(StateView):
    pass

class MctsState(StateView):
    def init(self):
        self.child_idx=0
        return super().init()

class Solution(SolutionBase):
    _has_view=True
    def get_cases(self):
        shape1_json=shape1(StateView).dump()
        return [
            dict(root=shape1_json, search_type="mcts", result=""),
            dict(root=StateView(
                StateView(
                    StateView().set_value(-2),
                    StateView().set_value(-4),
                ),
                StateView().set_value(-3)
            ).dump(), result=""),
            dict(root=StateView(
                StateView().set_value(-2),
                StateView().set_value(-3)
            ).dump(), result="")
        ]

    def get_watch(self):
        return [
            View("root").graph()
        ]

    def init(self, root, search_type="", **kw):
        self.kw=kw
        self.search_type = search_type
        # if search_type == 'mcts':
        #     self.root = MctsNode.load_from_json(**root).load()
        #     self.search_tree = MctsSearchTree()
        # else:
        #     self.root = AbNode.load_from_json(**root).load()
        #     self.search_tree = AlphaBateSearch()


    def execute(self):
        # return self.search_tree.search(self.root,**self.kw)
        pass


if __name__ == '__main__':
    Solution().run()
