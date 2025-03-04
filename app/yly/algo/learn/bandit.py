from common.algo.learn.env import Env
from common.algo.learn.bernoulli import Bernoulli
from common.algo.manage import SolutionBase
import random
import numpy as np
class Bandit(Env):
    k=10
    def reset(self):
        self.probs=np.random.uniform(size=self.k)
        self.max_prob=self.probs.max()
        self.actions=list(range(self.k))

    def do(self, action):
        return 0 if np.random.random()<self.probs[action] else 1
        

class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(tp=0,result="?")
        ]
    
    def init(self,tp):
        self.env=Bandit()
        self.actor:Bernoulli=[Bernoulli][tp]()
        self.actor.set_env(self.env).load()
    
    def execute(self,**kw):
        self.log(["%.2f"%float(v) for v in self.env.probs])
        self.log(sum(self.actor.run()))

if __name__=="__main__":
    np.random.seed(3)
    Solution().run()
        