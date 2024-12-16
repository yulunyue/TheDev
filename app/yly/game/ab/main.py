from ..game_base import GameBase,AI_KEY
from app.yly.algo.search.base import AbNode,shape1
import random
class AbGame(GameBase):
    def get_state(self):
        return shape1(AbNode)
    
    def dfs(self,key=None):
        def util(c:AbNode):
            if not c.childs:
                if key is None:
                    c.value = None
                elif key==c.k("value")["key"] and c.value is None:
                    c.calc_value(0)
            for n in c.childs:
                util(n)
        util(self.state)

    def login(self, user_id, **kw):
        self.dfs()
        return super().login(user_id, **kw)

    def open(self, key,**kw):
        self.dfs(key)
    
