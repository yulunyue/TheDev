from common.algo.search.state import State,TreeSearch
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
        return [ 'visits','value','score']
    
    def expand(self,n:State):
        self.expand_nodes[n.key]=n

    def fully_expanded(self):
        if len(self.expand_nodes) == len(self.childs):
            return True
        return False
    
    def __id__(self) -> int:
        return f'{self.value}{self.visits}{self.score}'

class MctsSearchTree(TreeSearch):
    def __init__(self) -> None:
        self.scalar=1/(2*math.sqrt(2.0))  #0.353553
        self.explore_ratio = 0
        self.root:MctsNode=None

    def expand(self, node:MctsNode):
        next_node=node.get_next()
        while next_node.has_childs() and next_node.key in node.expand_nodes:
            next_node=next_node.get_next()
        node.expand(next_node)
        return next_node

    def buck_up(self,node:MctsNode,value):
        self.root.cur = node
        while True:
            self.root.cur.visits+=1
            self.root.cur.value+=value
            if self.root.cur.parent is None:
                break
            self.root.cur=self.root.cur.parent

    def policy(self):
        self.root.cur = self.root
        while self.root.cur.has_childs():
            if not self.root.cur.expand_nodes:
                return self.expand(self.root.cur)
            elif random.uniform(0,1)<self.explore_ratio:
                self.root.cur = self.best_select(self.root.cur,self.scalar)
            elif not self.root.cur.fully_expanded():
                return self.expand(self.root.cur)
            else:
                self.root.cur=self.best_select(self.root.cur,self.scalar)
        return self.root.cur

    def best_select(self,node:MctsNode,scalar):
        best_score,bestchildren=-inf,[]
        for key,c in node.expand_nodes.items():
            c.score=self.get_score(node,c,scalar)
            if c.score == best_score:
                bestchildren.append(c)
            if c.score > best_score:
                bestchildren = [c]
                best_score=c.score
        return bestchildren[0]
            
    def get_score(self,p:MctsNode, node:MctsNode,scalar):
        exploit=p.get_value()/p.visits #平均值
        explore=math.sqrt(2.0*math.log(node.visits)/float(p.visits))    
        return exploit+scalar*explore

    def uct_seach(self,budget):
        for _ in range(budget):
            front=self.policy()
            self.buck_up(front, front.calc_value())
        return self.best_select(self.root,0)
    
    def search(self,root:MctsNode,budget=10,**kw):
        self.root = root
        return self.uct_seach(budget)