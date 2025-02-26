from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,logger
from common.algo.learn.env import Env
from common.algo.learn.dqn import Dqn
import numpy as np
ACTIONS=[[0,-1],[-1,0],[1,0],[0,1]]
ACS=['<','^','v','>']
class CfEnv(Env):
    def reset(self):
        self.actions=[0,1,2,3]
        self.size=4*12
        self.init_state = 12*3
        return self
    def do(self,state,aid):
        y,x=state//12,state%12
        y+=ACTIONS[aid][0]
        x+=ACTIONS[aid][1]
        if x<0 or y<0 or x>=12 or y==4:
            return False,-1,state
        s=y*12+x
        if s == 47:
            return 2,10,self.init_state
        if 36<s<47:
            return 1,-100,self.init_state
        return 0,-1,s
  
        


class D(Dqn):
    def __str__(self):
        def u(i,j):
            idx=np.argmax(self.q_table[i*12+j])
            return ACS[idx]
        return "\n".join(["".join([u(i,j) for j in range(12)]) for i in range(4)])

    # def update_qtable(self, state, action, reward, next_reward):
    #     info=f'{state},{ACS[action]}:{"%.2f"%self.q_table[state,action]} + {self.alpha}*({reward} + ({self.gamma_discount} * {next_reward}) - {"%.2f"%self.q_table[state,action]})'
    #     super().update_qtable(state, action, reward, next_reward)
    #     SolutionBase().log(f'{info}  ->  {"%.2f"%self.q_table[state,action]}')
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(result="?"),
        ]
    
    def init(self, *args, **kwargs):
        self.dqn=D(CfEnv().reset())
        
    def execute(self,**kw):
        records=self.dqn.run()
        self.log(self.dqn)
        for r,c,g in records:
            self.log(f'{g},{c},{"%.3f"%r}')


if __name__=='__main__':
    Solution().run()