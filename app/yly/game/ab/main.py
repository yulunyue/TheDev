from ..game_base import GameBase,AI_KEY

import random
class AbGame(GameBase):

    


    def login(self, user_id, **kw):
        self.dfs()
        return super().login(user_id, **kw)

    def open(self, key,**kw):
        self.dfs(key)
    
