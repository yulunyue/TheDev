from typing import List
from common.tool.debug_tool import Number, set_value
from common.game.game_base import PlayerBase, logger
from common.util.yml import yml_to_dict
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


class AlphaBateSearch:

    def evaluate(self):
        return 0

    def get_moves(self, depth, last_move):
        return []

    def do(self, *mv):
        pass

    def undo(self, *mv):
        return

    def search(self, depth=10, last_move=None, alpha=-inf, bate=inf) -> None:
        if depth == 0:
            return None, self.evaluate(depth, last_move)
        mvs = self.get_moves(depth, last_move)
        if not mvs:
            return None, self.evaluate(depth, last_move)
        best_mv = mvs[0]
        for mv in mvs:
            self.do(mv)
            _, val = self.search(depth=depth-1, last_move=mv,
                                 alpha=-bate, bate=-alpha)
            val = -val
            self.undo(mv)
            if val >= bate:
                alpha = set_value(alpha, bate)
                best_mv = mv
                break
            if val > alpha:
                alpha = set_value(alpha, val)
                best_mv = mv
        return best_mv, alpha


class AbNode(Number):
    def init(self):
        self.childs: List[AbNode] = []
        self._alpha: AbNode = None
        self._bate: AbNode = None
        return super().init()

    @property
    def alpha(self):
        if self._alpha is None:
            self._alpha = AbNode(f"{self.key}_al").set_value(-inf)
        return self._alpha

    @property
    def bate(self):
        if self._bate is None:
            self._bate = AbNode(f"{self.key}_ba").set_value(inf)
        return self._bate

    def set_children(self, childs):
        self.childs = childs
        return self

    def load_from_dict(self, mp: dict):
        v = mp.pop('_value')
        if v:
            self.set_value(int(v))
        for key, value in mp.items():
            self.childs.append(AbNode(key).load_from_dict(value))
        return self

    def load_from_yml(self, yml):
        return self.load_from_dict(yml_to_dict(yml))


class AlphaBateSearchDev(AlphaBateSearch, PlayerBase):

    def execute(self, i, env: AbNode):
        self.env = env
        best_mv, _ = self.search(alpha=env.alpha, bate=env.bate)
        return best_mv

    def evaluate(self, depth, mv: AbNode):
        return mv

    def get_moves(self, depth, last_move: AbNode):
        if last_move is None:
            return self.env.childs
        return last_move.childs
