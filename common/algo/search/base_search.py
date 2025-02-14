from typing import List
import random
inf = float("inf")
class State:
    def __init__(self) -> None:
        self.value = None
        self.depth = 0
        self.best_state:State=None
    
    def set_depth(self,depth):
        self.depth = depth
        return self
    

    def calc_value(self, *args):
        raise Exception("todo")

    def get_nexts(self,depth):
        return []
    
    def actor(self):
        pass

    def do(self):
        raise Exception("do")

    def undo(self):
        raise Exception("todo")
    
    def get_end(self):
        a=self.best_state
        while a.best_state:
            a=a.best_state
        return a
    
    
class TreeSearch:
    def search(self,state:State,depth=0):
        mvs:List[State]=state.get_nexts(depth)
        if not mvs:
            return state.calc_value()
        state.value = -inf
        for mv in mvs:
            mv.do()
            value=self.search(mv,depth+1)
            if value>state.value:
                state.value=value
                state.best_state=mv
            mv.undo()
        return state.value
    
    


