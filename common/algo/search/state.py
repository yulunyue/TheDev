from typing import List,Dict
import random
inf = float("inf")
class State:
    K=0
    def __init__(self) -> None:
        self.value = None
        self.depth = 0
        self.best_action=None
        self.next_state:Dict[int,State]=None
    
    def reset(self):
        return self

    def set_depth(self,depth):
        self.depth = depth
        return self
    
    def calc_value(self, *args):
        raise Exception("todo")

    def get_nexts(self,depth):# -> list:
        return dict()

    def get_bests(self):
        ret=[self]
        while ret[-1].best_action is not None:
            ret.append(ret[-1].next_state[ret[-1].best_action])
        return ret
    
    def is_game_over(self):
        raise Exception("todo")

    def do(self,action):
        raise Exception(f"{self.__class__}.do not impl")
    
    def get_regret(self,action):
        raise Exception("todo")
    


