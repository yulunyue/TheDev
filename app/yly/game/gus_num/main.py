from ..game_base import GameBase,AI_KEY
from collections import defaultdict
from common.service.http import Node
from typing import List,Dict
import random
class Ai(Node):
    def init(self):
        self.records=[]
        self.guas=[]
        self.set_data(records=self.records, guas=self.guas)
    
    def gauss(self,n):
        user_id,value=n.childs[0].key,''
        max_score=-100
        for c in n.childs:
            if c.key==self.key:
                continue
            score,num=self.calc(c.guas)
            if score>max_score:
                max_score=score
                value=num
                user_id=c.key
        return user_id,value
    
    def calc(self,gus):
        for v,c1,c2 in gus:
            pass
        return 0,'0000'

class GusNum(GameBase):         
    ai_gent:Ai
    cur_idx=None
    user:Dict[str,Ai]
    def get_data(self):
        return Ai()

    def reset(self):
        if AI_KEY not in self.user:
            self.ai_gent=self.user[AI_KEY]=Ai(key=AI_KEY)
            self.state.childs.append(self.ai_gent)
        self.cur_idx = None
        self.log('请所有玩家准备')
        for v in self.user.values():
            v.value=""
            v.records.clear()   
        self.ai_gent.value = "".join([str(random.randint(0,9)) for _ in range(4)])

    def set_num(self, user_id, user_id2, value):
        if self.user[user_id].value:
            return
        if len(value)!=4:
            return 
        if any(ord(v)<ord('0') or ord(v)>ord('9') for v in value):
            return 
        self.user[user_id].value = value
        ct=0
        for v in self.state.childs:
            ct+=0 if v.value else 1   
        self.log(f'{user_id} setnum xxxx rest {ct} man')
        if ct==0:
            self.cur_idx=1
            self.log(f'所有玩家已设置，游戏开始')
            self.log(f'请玩家 {self.state.childs[self.cur_idx].key} 猜测')
        
    def gauss_num(self, user_id, user_id2, value):
        if self.cur_idx is None:
            return
        if user_id != self.state.childs[self.cur_idx].key:
            return
        self.do(user_id,user_id2,value)
        if self.state.childs[self.cur_idx].key == AI_KEY:
            self.do(AI_KEY,*self.ai_gent.gauss(self.state))

    def do(self,user_id,user_id2,value):
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
        self.user[user_id2].guas.append([value,ct1,ct2])
        self.log(f'{user_id} gauss {user_id2} [{value}] result:[{ct1},{ct2}] ')
        self.log(f'{value}] result:[{ct1},{ct2}]',user_id2)
        if ct1==4:
            self.log(f'{user_id} win')
            self.reset()
        self.cur_idx=(self.cur_idx+1)%len(self.state.childs)
        
    def log(self,info,user_id=None):
        if user_id:
            self.user[user_id].records.append(info)
        else:
            self.state.records.append(info)

        
        


