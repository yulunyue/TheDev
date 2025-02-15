from typing import List,Dict
import random
inf = float("inf")
class State:
    def __init__(self) -> None:
        self.value = None
        self.depth = 0
        self.best_action=None
        self.next_state:Dict[int,State]=dict()
    
    def set_depth(self,depth):
        self.depth = depth
        return self
    

    def calc_value(self, *args):
        raise Exception("todo")

    def get_nexts(self,depth):
        return []
    
    def actor(self):
        pass


    
    def get_end(self):
        if self.best_action is None:
            return
        a=self.next_state[self.best_action]
        while a.best_action:
            a=a.next_state[a.best_action]
        return a
    
    
class TreeSearch:
    def search(self,state:State,depth=0):
        mvs:List[State]=state.get_nexts(depth)
        if not mvs:
            return state.calc_value()
        state.value = -inf
        for action,next_state in mvs:
            value=-self.search(next_state,depth+1)
            if value>state.value:
                state.value=value
                state.best_action=action
        return state.value
    
    


