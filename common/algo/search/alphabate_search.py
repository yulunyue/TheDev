from common.algo.search.base_search import TreeSearch,State,inf
from typing import List
class ABNode(State):
    def __init__(self):
        super().__init__()

class AlphaBateSearch:
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