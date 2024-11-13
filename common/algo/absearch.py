from typing import List
from common.tool.debug_tool import Number, set_value
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


class AbNode:
    KID = 0

    def __init__(self, key):
        self.key = key
        self.value = None
        self.childs: List[AbNode] = []
        self.alpha = -inf
        self.bate = inf

    def set_value(self, value):
        self.value = value
        return self

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

    def __str__(self) -> str:
        return f'[{self.key}:{self.value}]'

    def hex_str(self):
        res = f'{self.key}{self.value}{self.alpha}{self.bate}'
        return res+"".join(d.hex_str() for d in self.childs)

    def title2(self, key):
        from app.yly.algo.manage import wc
        return f'{key}: {wc("ti_"+str(self.key)+"_"+key, getattr(self,key))}'

    def get_title(self):
        from app.yly.algo.manage import wc
        sr = wc(f'self_arr_{self.key}', self.value)
        return '</br>'.join([
            f"{self.key}:->{self.value}",
            f"{self.title2('alpha')}, {self.title2('bate')}",
        ])

    def to_json(self):
        return dict(
            title=self.get_title(),
            childs=[v.to_json() for v in self.childs]
        )


class AlphaBateSearch:

    def evaluate(self, depth, last_move: AbNode):
        return last_move.value

    def get_moves(self, depth, last_move: AbNode):
        return last_move.childs

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
