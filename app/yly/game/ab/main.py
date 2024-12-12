from ..game_base import GameBase,AI_KEY
from app.yly.algo.search.base import AbNode,shape1
import random
class AbGame(GameBase):
    def get_data(self):
        return shape1(AbNode)
    
    def dfs(self,key=None):
        def util(c:AbNode):
            if len(c.childs):
                if key is None:
                    c.value = None
                elif key==c.key and c.value is None:
                    c.value = random.randint(-20,20)
            for n in c.childs:
                util(n)
        util(self.state)
    
    def reset(self,**kw):
        self.dfs()

    def open(self, key,**kw):
        self.dfs(key)
    
