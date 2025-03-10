from typing import List,Dict
import numpy as np
import random
inf = float("inf")
class Action:
    def __init__(self,action,state):
        self.key = action
        self.state:State=state
    def __str__(self):
        return f'{self.key}'
    
class State:
    K=0
    def __init__(self) -> None:
        self.value = None
        self.depth = 0
        self.best_action:Action=None
        self.next_state:List[int,State]=None
        self.parent:State=None
    
    def reset(self):
        return self

    def set_depth(self,depth):
        self.depth = depth
        return self
    
    def calc_value(self, *args):
        raise Exception("todo")

    def get_nexts(self,depth=None)->List[Action]:
        return []
    
    def get_random_next(self)->Action:
        k = len(self.get_nexts())
        return self.next_state[np.random.randint(0,k)]
    
    def get_bests(self):
        ret=[self]
        return ret
        n=self
        while n is not None:
            ret.append(n)
            if n.best_action:
                n=n.best_action.state
            else:
                break
            break
        return ret
    
    def is_game_over(self):
        raise Exception("todo")

    def do(self,action):
        raise Exception(f"{self.__class__}.do not impl")
    
    def get_regret(self,action):
        raise Exception("todo")
    
    @property
    def key(self):
        raise Exception("todo")
    

    


