from ..game_base import GameBase
from collections import defaultdict
from common.service.http import Node
from typing import List,Dict
class GusNum(GameBase):

        
    def set_num(self, user_id, user_id2, value):
        self.user[user_id].value = value

    def gauss_num(self, user_id, user_id2, value):
        ct1,ct2=0,0
        vt2=defaultdict(int)
        vt1=defaultdict(int)
        for i,v in enumerate(self.user[user_id2].value):
            if value[i]==v:
                ct1+=1
            else:
                vt2[v]+=1
                vt1[value[i]]+=1
        for v in vt1:
            ct2+=min(vt2[v],vt1[v])
        self.user[user_id].data = dict(ct1=ct1,ct2=ct2)
        
            


