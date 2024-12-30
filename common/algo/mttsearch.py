from common.algo.absearch import State
from typing import List,Dict
import math
import random
inf=float("inf")
class MctsNode(State):
    def __init__(self, *args):
        super().__init__(*args)
        self.visits = 0
        self.expand_nodes:Dict[str,MctsNode]=dict()
        self.score = 0
    
    def get_title_keys(self):
        return ['key', 'value', 'visits','score']
    
    def expand(self,n:State):
        self.expand_nodes[n.key]=n

    def fully_expanded(self):
        if len(self.expand_nodes) == len(self.childs):
            return True
        return False
    
    def __id__(self) -> int:
        return f'{self.value}{self.visits}{self.score}'

class MctsSearchTree:
    '''
    https://github.com/haroldsultan/MCTS/blob/master/mcts.py
    '''
    def __init__(self) -> None:
        self.scalar=1/(2*math.sqrt(2.0))
        self.explore_ratio = 0
        self.root:MctsNode=None

    def expand(self, node:MctsNode):
        next_node=node.get_next()
        while next_node.has_childs() and next_node.key in node.expand_nodes:
            next_node=next_node.get_next()
        node.expand(next_node)
        return next_node

    def buck_up(self,node:MctsNode,value):
        while node is not None:
            node.visits+=1
            node.value+=value
            node=node.parent

    def policy(self,node:MctsNode):
        while node.has_childs():
            if not node.expand_nodes:
                return self.expand(node)
            elif random.uniform(0,1)<self.explore_ratio:
                node = self.best_select(node,self.scalar)
            elif not node.fully_expanded():
                return self.expand(node)
            else:
                node=self.best_select(node,self.scalar)
        return node

    def best_select(self,node:MctsNode,scalar):
        bestscore,bestchildren=-inf,[]
        for key,c in node.expand_nodes.items():
            node.score=self.get_score(node,c,scalar)
            if node.score == bestscore:
                bestchildren.append(c)
            if node.score > bestscore:
                bestchildren = [c]
                bestscore=node.score
        return bestchildren[0]
            
    def get_score(self,c:MctsNode, node:MctsNode,scalar):
        exploit=c.get_value()/c.visits
        explore=math.sqrt(2.0*math.log(node.visits)/float(c.visits))    
        return exploit+scalar*explore

    def uct_seach(self,budget):
        for _ in range(budget):
            front=self.policy(self.root)
            self.buck_up(front, front.calc_value())
        return self.best_select(self.root,0)
    
    def search(self,root:MctsNode,budget=10,**kw):
        self.root = root
        return self.uct_seach(budget)