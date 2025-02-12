from typing import List
import random
inf = float("inf")
class State:
    def __init__(self) -> None:
        self.value = None
        self.depth = 0
    
    def set_depth(self,depth):
        self.depth = depth
        return self
    

    def calc_value(self, *args):
        raise Exception("todo")

    def get_nexts(self):
        pass
    

class TreeSearch:
    def __init__(self):
        pass
    def do(self, *mv):
        return self

    def undo(self, *mv):
        return self

    def search(self, last_move:State, depth=0, alpha=-inf, bate=inf,**kw) -> None:
        mvs:List[State] = last_move.get_nexts(depth)
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

