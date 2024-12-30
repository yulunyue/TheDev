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
    NODE_ID=0
    CUR=None
    def __init__(self,*args) -> None:
        self.key = State.NODE_ID
        State.NODE_ID+=1
        self.value = 0
        self.childs: List[State] = list(args)
        self.child_idx=0
        self.parent:State = None
        for d in self.childs:
            d.parent=self
        self.depth = 0
        self.init()

    def init(self):
        pass

    def has_childs(self):
        return len(self.childs)
    
    def get_next(self):
        State.CUR=self.childs[self.child_idx]
        self.child_idx=(self.child_idx+1)%len(self.childs)
        return State.CUR
    
    def calc_value(self, *args):
        return self.value
    
    def get_value(self,*args):
        return self.value
    
    def set_value(self,value):
        self.value = value
        return self
    
    def set_random_value(self,a=-10,b=10):
        random.seed(7)
        def dfs(c:State,depth):
            c.depth = depth
            if len(c.childs)==0:
                c.value=random.randint(a,b)            
                return c.value
            c.value=0
            for v in c.childs:
                c.value+=dfs(v,depth+1)
            return c.value
        dfs(self,0)       
        return self
    
    def get_title_keys(self):
        return ['key','value']
    
    def dump(self):
        return dict(
            value=self.value,
            childs=[v.dump() for v in self.childs]
        )
    
    def tree_view(self):
        from app.yly.algo.manage import color
        return dict(
            data=[
                self.k(k) for k in self.get_title_keys()
            ],
            childs=[c.tree_view() for c in self.childs],
            key=f"search_state_{self.key}",
            color=color(self,State.CUR),
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
    
    def __id__(self) -> int:
        return f'{self.value}'
    
    def __str__(self) -> str:
        cur_key=str(State.CUR.key if State.CUR else '')
        return cur_key+self.__id__()+"".join([v.__id__() for v in self.childs])
    
    @classmethod
    def load_from_json(cls,value,childs,depth=0,**kw):
        return cls(
            *[cls.load_from_json(**d) for d in childs]
        ).set_value(value)
    
class AbNode(State):
    def init(self):
        self.alpha = -inf
        self.bate = inf
    
class AlphaBateSearch:

    def get_moves(self, depth, last_move: AbNode):
        return last_move.childs

    def do(self, *mv):
        return self

    def undo(self, *mv):
        return self

    def search(self, last_move:AbNode, depth=10, alpha=-inf, bate=inf,**kw) -> None:
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

