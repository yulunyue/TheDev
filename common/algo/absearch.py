from typing import List
import random
inf = float("inf")

'''
                                           a:4
                                           min                                
          b:2                  c:6                    d:3             e:2            
          max                  max                    max
    f:8   g:2   h:7       i:1  j:4?  k:2?      l:3    m:6   n:9
    min
o:8     p:9                                                 
'''



class AbNode:
    NODE_ID=0
    def __init__(self, *args):
        self.key = AbNode.NODE_ID
        AbNode.NODE_ID+=1
        self.value = None
        self.childs: List[AbNode] = list(args)
        self.alpha = -inf
        self.bate = inf
        self._value =  None

    def set_value(self,value):
        self._value=value
        return self
    
    @staticmethod
    def load_from_json(value,childs,depth=0,**kw):
        ret = AbNode().set_value(value)
        ret.depth = depth
        for v in childs:
            ret.childs.append(AbNode.load_from_json(depth=depth+1,**v))
        return ret
    
    def init(self,depth=0):
        self.depth = depth            
        for v in self.childs:
            v.init(depth+1)        
        return self
    
    def k(self, name):
        from app.yly.algo.manage import bp
        if not name:
            value = f'{self.key}'
            if self.childs:
                value+=[":Y",":Z"][self.depth%2]
            #value = self.key
        else:
            value = getattr(self,name)
        return bp(name ,value,f"Ab_Node_{self.key}")
    

    def set_children(self, childs):
        self.childs = childs
        return self

    def get_title_keys(self):
        if not self.childs:
            return ['','value']
        return ['','alpha','bate']

    def tree_view(self):
        return dict(
            data=[
                self.k(k) for k in self.get_title_keys()
            ],
            childs=[c.tree_view() for c in self.childs],
            key=f"Ab_Nd_{self.key}"
        )
    
    def graph_view(self):
        return self.tree_view()
    
    def __str__(self) -> str:
        ret=f'[{self.value}{self.alpha}{self.bate}]'
        return ret+"".join([str(v) for v in self.childs])

    def dump(self):
        return dict(
            value=self._value,
            childs=[v.dump() for v in self.childs]
        )

    def to_json(self):
        return self.tree_view()
    
    def calc_value(self, depth):
        if self._value is not None:
            self.value = self._value
        else:
            self.value = random.randint(-5,5)
        return self
    
    

class AlphaBateSearch:

    def get_moves(self, depth, last_move: AbNode):
        return last_move.childs

    def do(self, *mv):
        return self

    def undo(self, *mv):
        return self

    def search(self, last_move:AbNode, depth=10, alpha=-inf, bate=inf) -> None:
        if depth == 0:
            return last_move.calc_value(depth)
        mvs = self.get_moves(depth, last_move)
        if not mvs:
            return last_move.calc_value(depth)
        last_move.alpha, last_move.bate = alpha, bate
        for mv in mvs:
            self.do(mv)
            self.search(mv,depth=depth-1,
                                 alpha=-last_move.bate, bate=-last_move.alpha)
            self.undo(mv)
            if mv.value >= last_move.bate:
                last_move.alpha = last_move.bate
                break
            if mv.value > last_move.alpha:
                last_move.alpha = mv.value
        return last_move.alpha

