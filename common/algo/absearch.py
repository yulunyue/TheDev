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

class State:
    root = None
    def __init__(self) -> None:
        self.value =None
        self.depth = 0
        self.init()
    
    def set_depth(self,depth):
        self.depth = depth
        return self
    
    def init(self):
        pass

    def get_value(self):
        return None
    
    def set_value(self,*args):
        return self
    
    def calc_value(self, *args):
        raise Exception("todo")

    def get_title_keys(self):
        return ['key','value']
    
    def dump(self):
        return dict(
            value=self.get_value(),
            childs=[v.dump() for v in self.get_nexts()]
        )
    
    def tree_view(self):
        from app.yly.algo.manage import color
        return dict(
            data=[
                self.k(k) for k in self.get_title_keys()
            ],
            childs=[c.tree_view() for c in self.get_nexts(self.depth)],
            key=f"search_state_{self.key}",
            color=color(self,self.root.cur if self.root and self.root.cur else None),
        )
    
    def graph_view(self):
        return self.tree_view()
    
    def k(self, name):
        from app.yly.algo.manage import bp
        value = getattr(self,name)
        return bp(name ,value,f"Node_{self.key}")
    
    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        return value.key==self.key
    
    
    @classmethod
    def load_from_json(cls,value,childs,depth=0,**kw):
        return cls(
            *[cls.load_from_json(**d) for d in childs]
        ).set_value(value)
    
    def get_nexts(self,depth):
        raise Exception("todo")
    
class AbNode(State):
    def init(self,*args):
        self.alpha = -inf
        self.bate = inf
        self.best_action:AbNode=None

class AlphaBateSearch:
    def __init__(self):
        pass
    def do(self, *mv):
        return self

    def undo(self, *mv):
        return self

    def search(self, last_move:AbNode, depth=0, alpha=-inf, bate=inf,**kw) -> None:
        mvs:List[AbNode] = last_move.get_nexts(depth)
        if not mvs:
            return last_move.calc_value(depth)
        last_move.alpha, last_move.bate = alpha, bate
        for mv in mvs:
            self.do(mv)
            mv.value=-self.search(mv,depth=depth+1,
                                 alpha=-last_move.bate, bate=-last_move.alpha)
            self.undo(mv)
            if mv.value >= last_move.bate:
                last_move.alpha = last_move.bate
                last_move.best_action=mv
                break
            if mv.value > last_move.alpha:
                last_move.alpha = mv.value
                last_move.best_action=mv
        return last_move.alpha

