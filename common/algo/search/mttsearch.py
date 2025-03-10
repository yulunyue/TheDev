from common.algo.search.state import State,Action
from common.algo.search.algo import Algo
from typing import List,Dict
import math
import random
import numpy as np

inf=float("inf")
class MctsNode(State):
    def __init__(self, *args):
        super().__init__(*args)
        self.visits = 0
        self.score = 0
        self.vt_num=0
        self.mct_value = 0
        self.expand_nodes:Dict[str,Action] = {}

    def fully_expanded(self):
        return self.vt_num>=len(self.get_nexts())




class MctsSearchTree(Algo):
    def __init__(self) -> None:
        self.scalar=1/(2*math.sqrt(2.0))  #0.353553
        self.explore_ratio = 0

    def expand(self, state:MctsNode):
        action = state.get_random_next()
        while action.key in state.expand_nodes:
            action.state.parent=state
            state=action.state
            action=state.get_random_next()
        if action.key not in state.expand_nodes:
            state.expand_nodes[action.key]=action
            action.state.parent=state
            return action.state
        return action.state

    def buck_up(self,node:MctsNode,value):
        while True:
            node.visits+=1
            node.mct_value+=value
            if node.parent is None:
                break
            node=node.parent

    def policy(self,cur:MctsNode):
        while cur.get_nexts():
            if not cur.expand_nodes or np.random.rand()>self.explore_ratio:
                return self.expand(cur)
            else:
                cur=self.best_select(cur,self.scalar)
        return cur

    def best_select(self,node:MctsNode,scalar):
        best_score=-inf
        for a in node.expand_nodes.values():
            score=self.get_score(node,a.state,scalar)
            if node.best_action is None or score is None:
                node.best_action=a
            elif score > best_score:
                node.best_action=a
                best_score=score
      
            
    def get_score(self,p:MctsNode, node:MctsNode,scalar):
        if not p.visits:
            return None
        exploit=p.mct_value/p.visits #平均值
        explore=math.sqrt(2.0*math.log(node.visits)/p.visits)    
        return exploit+scalar*explore

    def uct_seach(self, node, budget):
        for _ in range(budget):
            front=self.policy(node)
            self.buck_up(front, front.calc_value())
        self.best_select(node,0)
    
    def search(self,root:MctsNode,budget=10,**kw):
        self.uct_seach(root,budget)