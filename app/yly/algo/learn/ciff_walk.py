from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.learn.env import Env
from common.algo.learn.dqn import Dqn
import numpy as np
ACTIONS=[[0,1],[0,-1],[-1,0],[1,0]]
class CfEnv(Env):
    def reset(self):
        self.actions=[0,1,2,3]
        self.size=4*12
        self.state = 12*3+0
        return self
    def do(self,aid):
        state=self.state+12*ACTIONS[aid][0]+ACTIONS[aid][1]
        if state == 47:
            return True,10
        if 36<state<47:
            return True,-100
        return False,-1


class D(Dqn):
    def __str__(self):
        def u(i,j):
            idx=np.argmax(self.q_table[i*12+j])
            return ['R','L','U','D'][idx]
        return "\n".join(["".join([u(i,j) for j in range(12)]) for i in range(4)])
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(result="?"),
        ]
    
    def init(self, *args, **kwargs):
        self.dqn=D(CfEnv().reset())
        
    def execute(self,**kw):
        self.dqn.run()
        self.log(self.dqn)


if __name__=='__main__':
    Solution().run()