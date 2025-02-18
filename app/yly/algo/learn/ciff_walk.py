from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
from common.algo.learn.env import Env
from common.algo.learn.dqn import Dqn
from common.algo.learn import np
class CfEnv(Env):
    def reset(self):
        self.actions=[0,1,2,3]
        self.map=np.zeros((4,12))
        self.size=4*12
        self.state = 12*3+0
        return self

class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(result=""),
        ]
    
    def init(self, *args, **kwargs):
        self.dqn=Dqn(CfEnv())
        
    def execute(self,**kw):
        self.dqn.run()


if __name__=='__main__':
    Solution().run()