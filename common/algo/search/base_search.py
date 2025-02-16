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


    def get_bests(self):
        ret=[self]
        while ret[-1].best_action is not None:
            ret.append(ret[-1].next_state[ret[-1].best_action])
        return ret
    
    
class TreeSearch:
    def search(self,state:State,depth=0):
        mvs:List[State]=state.get_nexts(depth)
        if not mvs:
            return state.calc_value(depth)
        state.value = -inf
        for action,next_state in mvs:
            value=-self.search(next_state,depth+1)
            if value>state.value:
                state.value=value
                state.best_action=action
        return state.value
    
    


